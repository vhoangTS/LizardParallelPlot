import os

def getVariantspath(modelPath,reportfname):
    """list dirs in modelPath in order to get variant names and its folder path"""
    vnames = [name for name in os.listdir(modelPath) if os.path.isdir(os.path.join(modelPath,name))]
    vpath = [os.path.join(modelPath,name) for name in os.listdir(modelPath) if os.path.isdir(os.path.join(modelPath,name))]
    return vnames,vpath

def getoutputID(line,searchsignal):
    """get index/location of searchsignal in line"""
    line0 = line.split()
    SID = None
    for sid,item in enumerate(line0):
        if searchsignal in item:
            SID = sid
            break
    return SID #this is not a very safe way of doing it

def getSUMresults(filepath,searchsignal):
    """return sum/total value of searchsignal"""
    OutputFile = open(filepath,"r")
    OutputLines = OutputFile.readlines()
    OutputFile.close()
    SID = getoutputID(OutputLines[1],searchsignal)
    results = []
    for line in OutputLines:
        line = line.split()
        try:
            hour = float(line[0]) #should be between 1-8760
            results.append(float(line[SID]))
        except:
            pass
    return sum(results)

def illCAL(illline,thres):
    """Calculating sDA, %of DF based on ill line"""
    illline = illline.split()
    nrpts = len(illline)-1
    count = 0
    for value in illline[1:]:
        if float(value) >= thres:
            count +=1
    percentage = round(count/nrpts * 100,0)
    return percentage

def getsDA(illfile):
    """read Ill file and return sDA300,50
    In this case also returning % of floor area has DF larger than 3%"""
    illf = open(illfile,"r")
    illlines = illf.readlines()
    illf.close()
    for line in illlines:
        if "DA_300" in line and "CDA" not in line:
            DAline = line
        elif "DF" in line:
            DFline = line
    #sDA calculation
    sDA = illCAL(DAline,50)
    sDF = illCAL(DFline,3)
    return sDA,sDF

def ReadAndWriteReport(modelPath,reportfname):
    #extract all file paths
    vnames, vpath = getVariantspath(modelPath,reportfname)
    addOutput = [os.path.join(fpath,"Results\\AddOutput_1h.prn") for fpath in vpath]
    illfile = [os.path.join(fpath,"Daylight\\001_Z1.ill") for fpath in vpath]
    #read files and write reports
    reportf = open(os.path.join(modelPath,reportfname),"w")
    #first line
    reportf.write("Varname\tOrientation\tWWR\tSHDActive\tTotalRadOnWindow\tTotalRadThroughWindow\tTotalInternalGain\tTotalHeating\tTotalCooling\tTotalEnergy\tDaylightFactor\tSpatialDaylightAutonomy\n")
    for vid,va in enumerate(vnames):
        reportf.write("%s\t"%(va))
        reportf.write("%s\t"%(va.split("_")[0]))
        reportf.write("%s\t"%(va.split("_")[1]))
        reportf.write("%s\t"%(round(getSUMresults(addOutput[vid],"SHD_active"),0)))
        reportf.write("%s\t"%(round(getSUMresults(addOutput[vid],"IT_")/3600,0)))
        reportf.write("%s\t"%(round(getSUMresults(addOutput[vid],"QSOLTR_")/3600,0)))
        reportf.write("%s\t"%(round(getSUMresults(addOutput[vid],"Q_intgain_")/1000,0)))
        reportf.write("%s\t"%(round(getSUMresults(addOutput[vid],"Q_tot_ht_")/1000,0)))
        reportf.write("%s\t"%(round(getSUMresults(addOutput[vid],"Q_tot_cl_")/1000,0)))
        reportf.write("%s\t"%(round(getSUMresults(addOutput[vid],"Q_tot_ht_")/1000 + getSUMresults(addOutput[vid],"Q_tot_cl_")/1000,0)))
        sda,sdf = getsDA(illfile[vid])
        reportf.write("%s\t"%(sdf))
        reportf.write("%s\n"%(sda))
    reportf.close()
