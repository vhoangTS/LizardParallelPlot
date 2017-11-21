import os
import sys
import plotly as py
import plotly.graph_objs as go
from reportWriter import *

def getTagID(line,tagname):
    """Get id of a label based on its name, later used to extract data in line"""
    tagID = None
    newline = line.split()
    for tid,item in enumerate(newline):
        #print(item)
        if tagname in item:
            tagID = tid
        else:
            pass
    return tagID

def getValues(reportLines,tagname):
    """Get values as dict {tagname:[list if values]}"""
    Values = dict()
    Values[tagname] = []
    #get id from first line
    ValueID = getTagID(reportLines[0],tagname)
    for line in reportLines[1:]:
        line = line.split()
        try:
            Values[tagname].append(round(float(line[ValueID]),0))
        except (ValueError,TypeError):
            Values[tagname].append(line[ValueID])
    return Values

def assignDict(inputdict,nrtick = 6):
    """Generating dictionary for plotting"""
    label = list(inputdict.keys())
    values = inputdict[label[0]]
    vrange = [min(values),max(values)]
    return dict(range = vrange, label = label[0], values = values)

def parallelPlot():
    """Plot parallel graph for selected variants"""
    data = [
        go.Parcoords(
            line = dict(color = WWR["WWR"],
                        colorscale = 'RdBu',
                        showscale = False, #True to show colorscale legend
                        reversescale = False,
                        ),
            dimensions = list([
                dict(range=[0,5],
                     tickvals =[1,2,3,4],
                     label = "Orientation",
                     values = plotOri,
                     ticktext = ['East','North','South','West']),
                assignDict(WWR),
                assignDict(ShadingActive),
                assignDict(TotalRadWindow),
                assignDict(TotalRadEnteredWindow),
                assignDict(TotalIntGain),
                assignDict(TotalHeating),
                assignDict(TotalCooling),
                assignDict(TotalEnergy),
                assignDict(DF),
                assignDict(sDA)
            ])
        )
    ]
    layout = go.Layout(width = 1880,height = 888) #plot_bgcolor = '#E5E5E5', paper_bgcolor = '#E5E5E5'

    fig = go.Figure(data = data, layout = layout)
    py.offline.plot(fig,filename = "parallel.html")

###Start here
modelPath = "p:\\Giessen_Wohnen_am_alten_Flughafen_170128\\Sim_Thermal\\20171116_WWR_study\\Model\\"
reportfname = "VARIANT_REPORT.txt"
rewriteFile = False #True to rewrite report file

#write report file only if needed (signal == True or there's no report file)
if rewriteFile or not os.path.isfile(os.path.join(modelPath,reportfname)):
    ReadAndWriteReport(modelPath,reportfname)
else:
    pass
reportPath = os.path.join(modelPath,reportfname)

#read report file
reportFile = open(reportPath,"r")
reportLines = reportFile.readlines()
#extract all data
variants = getValues(reportLines,"Varname")
orientation = getValues(reportLines,"Orientation")
WWR = getValues(reportLines,"WWR")
ShadingActive = getValues(reportLines,"SHDActive")
TotalRadWindow = getValues(reportLines,"TotalRadOnWindow")
TotalRadEnteredWindow = getValues(reportLines,"TotalRadThroughWindow")
TotalIntGain = getValues(reportLines,"TotalInternalGain")
TotalHeating = getValues(reportLines,"TotalHeating")
TotalCooling = getValues(reportLines,"TotalCooling")
TotalEnergy = getValues(reportLines,"TotalEnergy")
DF = getValues(reportLines,"DaylightFactor")
sDA = getValues(reportLines,"SpatialDaylightAutonomy")
reportFile.close()
plotOri = []
for item in orientation['Orientation']:
    if item == 'E':
        plotOri.append(1)
    elif item == 'N':
        plotOri.append(2)
    elif item == 'S':
        plotOri.append(3)
    elif item == 'W':
        plotOri.append(4)

#here plotting start for selected variants
parallelPlot()
