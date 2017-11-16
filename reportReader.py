import os
import sys

import plotly as py
import plotly.graph_objs as go

reportPath = "c:\\Users\\vhoang\\Desktop\\LizardParallelPlot\\20171611_WWR_data.txt"

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




reportFile = open(reportPath,"r")
reportLines = reportFile.readlines()
#extract data
variants = getValues(reportLines,"VARIANT")
orientation = getValues(reportLines,"Orientation")
WWR = getValues(reportLines,"WWR")
ShadingActive = getValues(reportLines,"ShadingActive")
TotalRadWindow = getValues(reportLines,"TotalRadiationOnWindow")
TotalRadEnteredWindow = getValues(reportLines,"TotalRadiationThroughWindow")
TotalIntGain = getValues(reportLines,"TotalInternalGain")
TotalHeating = getValues(reportLines,"TotalHeating")
TotalCooling = getValues(reportLines,"TotalCooling")
TotalEnergy = getValues(reportLines,"TotalEnergy")
DF = getValues(reportLines,"DF3")
sDA = getValues(reportLines,"sDA300lux")
reportFile.close()



data = [
    go.Parcoords(
        line = dict(color = WWR["WWR"],
                    colorscale = 'Jet',
                    showscale = True,
                    reversescale = False,
                    cmin = 15,
                    cmax = 60),
        dimensions = list([
            assignDict(WWR),
            #assignDict(ShadingActive),
            #assignDict(TotalRadWindow),
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

layout = go.Layout() #plot_bgcolor = '#E5E5E5', paper_bgcolor = '#E5E5E5'

fig = go.Figure(data = data, layout = layout)
py.offline.plot(fig,filename = "parallel.html")

