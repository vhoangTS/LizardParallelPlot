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
            Values[tagname].append(float(line[ValueID]))
        except (ValueError,TypeError):
            Values[tagname].append(line[ValueID])
    return Values


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
TotaCooling = getValues(reportLines,"TotalCooling")
TotalEnergy = getValues(reportLines,"TotalEnergy")
DF = getValues(reportLines,"DF3")
sDA = getValues(reportLines,"sDA300lux")
reportFile.close()

data = [
    go.Parcoords(
        line = dict(color = WWR["WWR"],
        colorscale = [[15,"#439ACA"],[30,"#E9743F"],[40,"#36C2A6"],[45,"#FEDE86"],[50,"#EC696D"],[55,"#2C0260"],[60,"#6E07F2"]]),
        dimensions = list([
            dict(range = [0,100],
                 label = "WWR",
                 values = WWR["WWR"]),
            dict(range = [0,100],
                 label = "DF",
                 values = DF["DF3"]),
            dict(range = [0,100],
                 label = "sDA",
                 values = sDA["sDA300lux"])
        ])
    )
]

layout = go.Layout() #plot_bgcolor = '#E5E5E5', paper_bgcolor = '#E5E5E5'

fig = go.Figure(data = data, layout = layout)
py.offline.plot(fig,filename = "parallel.html")

