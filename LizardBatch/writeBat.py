import os

modelPath = "p:\\Giessen_Wohnen_am_alten_Flughafen_170128\\Sim_Thermal\\20171116_WWR_study\\Model\\"
trnsysPath ="w:\\Trnsys18\\"
batchfile = "RUNALL.bat"

#choose what to run
runRAD = True
runVFM = True
runSHM = True

def getVariants(modelPath):
    """get file variant names and respectively the b18,d18 file paths"""
    variants = [name for name in os.listdir(modelPath) if os.path.isdir(os.path.join(modelPath,name))]
    b18file = [os.path.join(modelPath,"%s\\%s.b18"%(vname,vname)) for vname in variants]
    d18file = [os.path.join(modelPath,"%s\\%s.d18"%(vname,vname)) for vname in variants]
    return variants,b18file,d18file

def getTRNSYS(trnsysPath):
    """get path to trnbuild, trnrad and trnexe"""
    trnBUILD = os.path.join(trnsysPath,"Building\\TRNBuild.exe")
    trnRAD = os.path.join(trnsysPath,"Building\\trnRAD\\trnRAD.exe")
    trnEXE = os.path.join(trnsysPath,"Exe\\TrnEXE64.exe")
    return trnBUILD,trnRAD,trnEXE

def writeBat(b18file,d18file,runRAD,runVFM,runSHM):
    batfile = open(os.path.join(modelPath,batchfile),"w")
    for vid,b18 in enumerate(b18file):
        if runRAD:
            batfile.write("%s\t%s\n"%(trnRAD,b18)) #run trnRAD to generate dc files
        if runVFM:
            batfile.write("%s\t%s\t/N\t/vfm\n"%(trnBUILD,b18)) #generate vfm files
        if runSHM:
            batfile.write("%s\t%s\t/N\t/masks\n"%(trnBUILD,b18)) #generate shm files
        batfile.write("%s\t%s\t/N\t/save\n"%(trnBUILD,b18)) #save b18 file
        batfile.write("%s\t%s\t/N\t/h\n"%(trnEXE,d18file[vid])) #run simulation /h to hide online plotter, /N to exit online plotter after finished
    batfile.close()

#here it start
variants,b18file,d18file = getVariants(modelPath)
trnBUILD,trnRAD,trnEXE = getTRNSYS(trnsysPath)

#writing batch file for all variants
writeBat(b18file,d18file,runRAD,runVFM,runSHM)
