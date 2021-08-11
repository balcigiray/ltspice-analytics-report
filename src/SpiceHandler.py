# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 13:01:20 2021

@author: Giray Balcı
"""

class SpiceHandler:
    import os
    import subprocess
    import time
    import re
    from Components import Component, Component2Pin, Capacitor, Resistor, BJT
    
    measVRMS = ".meas %s+VRMS RMS V"
    measVMAX = ".meas %s+VMAX MAX V"
    measIRMS = ".meas %s+IRMS RMS I"
    measIMAX = ".meas %s+IMAX MAX I"
    measPAVG = ".meas %s+PAVG AVG V"
    measPMAX = ".meas %s+PMAX MAX V"
    
    regexMeasName = ".+(?=:)"
    regexMeasValue = "(?<==).+?(?= )"  #(?<==).+[^ ](?= )

    def __init__(self, exeLocation, exeName, fileName):
        if(fileName[-4:] == ".asc" ):
            self.fileName = fileName
            self.exeLocation = exeLocation
            self.exeName = exeName
        else:
            print("Error in file extension")
            
        self.listOfComponents = []
        
        self.__createNetFile()
        self.__createTxtFile()
        self.__clearUnnecassaryFiles()


    # create a initial call for asc file to auto create .net file.
    # Wait a little bit, then, close LTSpice
    def __createNetFile(self):
        self.subprocess.Popen(self.exeLocation + self.exeName + " -Run " + self.fileName)
        self.time.sleep(2)
        self.os.system("taskkill /im " + self.exeName + " /F" )
        
    
    # Create txt file using .net file
    def __createTxtFile(self):
        netFileName = self.fileName[:-3] + "net"
        with open(netFileName, 'rb') as file:  # Read in the file as binary data
            self.spiceData = file.read().decode("ascii")
            file.close()
            
        txtFileName = self.fileName[:-3] + "txt"
        with open(txtFileName, 'wb') as file:  # Write a file as binary data
            file.write(self.spiceData.encode("ascii"))
            file.close()
  
        print(txtFileName + " created")
            
    
    # Delete by-product files
    def __clearUnnecassaryFiles(self):
        extensions = ["log", "op.raw", "raw"]
        
        for e in extensions:
            toDelete = self.fileName[:-3] + e
            if self.os.path.exists(toDelete):
                self.time.sleep(1)
                self.os.remove(toDelete)
            else:
                print("File does not exist")
                
                
    def getComponentList(self):
        spiceLines = self.spiceData.splitlines()
        spiceComponentLines = []

        for l in spiceLines:
            if(self.re.match("^[a-jA-Jl-zL-Z]", l)):
                spiceComponentLines.append(l)
                
        print("Number of all components: " + str(len(spiceComponentLines)))
     
        #individual list of components
        listResistors = []
        listCapacitors = []
        listBJTs = []
        
        #seperate components into their own lists        
        for l in spiceComponentLines:
            atoms = l.upper().split()
            
            if(atoms[0].startswith("R")):
                res = self.Resistor(atoms[0], atoms[1], atoms[2], atoms[3])
                
                listResistors.append(res)
            if(atoms[0].startswith("C")):
                cap = self.Capacitor(atoms[0], atoms[1], atoms[2], atoms[3])
                listCapacitors.append(cap)                
            if(atoms[0].startswith("Q")):
                bjt = self.BJT(atoms[0], atoms[1], atoms[2], atoms[3], atoms[5])
                listBJTs.append(bjt) 
                                   
        print("Number of resistors: " + str(len(listResistors)))        
        print("Number of capacitors: " + str(len(listCapacitors)))
        print("Number of BJTs: " + str(len(listBJTs)))
                
        self.listOfComponents.append(listResistors)
        self.listOfComponents.append(listCapacitors)
        self.listOfComponents.append(listBJTs)
        
        return self.listOfComponents
    
    
    def generateMeasCommand(self):
        resistors = self.listOfComponents[0]
        capacitors = self.listOfComponents[1] 
        bjts = self.listOfComponents[2] 
        
        measCMD = ""

        for r in resistors:
            measCMD += r.createMeasCommandVol(self.measVRMS)
            measCMD += r.createMeasCommandVol(self.measVMAX)
            measCMD += r.createMeasCommandCur(self.measIRMS)
            measCMD += r.createMeasCommandCur(self.measIMAX)  
            measCMD += r.createMeasCommandPow(self.measPAVG)
            measCMD += r.createMeasCommandPow(self.measPMAX)              
            
        for c in capacitors:
            measCMD += c.createMeasCommandVol(self.measVRMS)
            measCMD += c.createMeasCommandVol(self.measVMAX)
            measCMD += c.createMeasCommandCur(self.measIRMS)
            measCMD += c.createMeasCommandCur(self.measIMAX) 
            
        for b in bjts:
            measCMD += b.createMeasCommandVol(self.measVRMS)
            measCMD += b.createMeasCommandVol(self.measVMAX)
            measCMD += b.createMeasCommandCur(self.measIRMS, "Q")
            measCMD += b.createMeasCommandCur(self.measIMAX, "Q")
            
        return measCMD
    
    
    def createNewSimFile(self, measCommand):
        splitData = self.spiceData.split(".backanno")
        endOfFile = ".backanno \n.end"
        endFile = splitData[0] + measCommand + endOfFile
        
        self.measFileName = self.fileName[:-4] + "_meas.txt"
        
        with open(self.measFileName, 'wb') as file:  # Write a file as binary data
            file.write(endFile.encode('ascii'))
            file.close()  
            
        return self.measFileName

    
    def runSimulation(self, name):
        self.subprocess.call(self.exeLocation +  self.exeName + " -b " + name)
        
    
    def getSimulationResults(self):
        name = self.measFileName[:-3] + "log"
               
        with open(name, 'rb') as file:  # Read in the file as binary data
            measurements = file.read().decode('ascii')
            file.close()
        
        measurementLines = measurements.splitlines()[4:-19] #should check if all applies
        
        for l in measurementLines:
            measName = self.re.search(self.regexMeasName, l).group() #r5+vrms
            mn = measName[:-5].upper().split("+") #R5
            name = mn[0] #R5
            measType = measName[-4:].upper() #VRMS
            
            valueText = self.re.search(self.regexMeasValue, l).group() #0.651136
            value = float(valueText)

            for li in self.listOfComponents:
                for co in li:
                    if(co.name == name):
                        if (co.numberOfNodes == 2):    
                            co.addMeasurement("P1P2", measType, value)
                        elif(co.numberOfNodes == 3): 
                            co.addMeasurement(measType[0]+mn[1], measType, value)
            
        return self.listOfComponents

