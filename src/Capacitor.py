# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 17:24:16 2021

@author: Giray Balcı
"""

class Capacitor:
    def __init__(self, name, node1, node2, value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = value
        self.type = "capacitor"
        self.numberOfMeas = 0
        
        
    def createMeasCommandVol(self, measCommand):
        measText = ""
        
        if(self.node2 == "0"): #if node is connected to ground
            measText = measText + measCommand % (self.name) + "(%s)\n" % (self.node1)
        else:
            measText = measText + measCommand % (self.name) + "(%s,%s)\n" % (self.node1, self.node2)          
  
        return measText


    def createMeasCommandCur(self, measCommand):
        measText = ""
        measText = measText + measCommand % (self.name) + "(%s)\n" % (self.name)
        
        return measText
    
    
    def addMeasurement(self, keyword, measurement):
        if(keyword == "VRMS"):
            self.vrms = measurement
            self.numberOfMeas += 1
        if(keyword == "VMAX"):
            self.vmax = measurement
            self.numberOfMeas += 1
        if(keyword == "IRMS"):
            self.irms = measurement
            self.numberOfMeas += 1
        if(keyword == "IMAX"):
            self.imax = measurement
            self.numberOfMeas += 1
            