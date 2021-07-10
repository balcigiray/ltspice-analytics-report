# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 17:24:16 2021

@author: Giray Balcı
"""

class Capacitor:
    measVRMS0 = ".meas %s_VRMS RMS V(%s)\n"
    measVRMS = ".meas %s_VRMS RMS V(%s,%s)\n"
    measVMAX0 = ".meas %s_VMAX MAX V(%s)\n"
    measVMAX = ".meas %s_VMAX MAX V(%s,%s)\n"    
    
    
    def __init__(self, name, node1, node2, value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = value
        
    def createMeasCommand(self):
        measText = ""
        
        if(self.node2 == "0"): #if node is connected to ground
            measText = measText + self.measVRMS0 % (self.name, self.node1)
            measText = measText + self.measVMAX0 % (self.name, self.node1)            
        else:
            measText = measText + self.measVRMS % (self.name, self.node1, self.node2)            
            measText = measText + self.measVMAX % (self.name, self.node1, self.node2)   
        
        return measText
    
    def addMeasurement(self, keyword, measurement):
        if(keyword == "VRMS"):
            self.vrms = measurement
        if(keyword == "VMAX"):
            self.vmax = measurement