# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 12:50:03 2021

@author: Giray Balcı
"""

class Component:
    name = ""
    nodes = None
    value = ""
    compType = ""
    measurements = None
    numberOfNodes = None
    
    def __init__(self, name, value, compType, numNode):
        self.name = name
        self.value = value
        self.compType = compType
        self.nodes = list()
        self.measurements = dict()        
        self.numberOfNodes = numNode
        
        
    def addNode(self, node):
        self.nodes.append(node)
        
        
    def addMeasurement(self, keyword, measType, measurement):
        l = dict()
        l[measType] = measurement
 
        i = self.measurements.get(keyword, l)
        i[measType] = measurement
        self.measurements[keyword] = i



class Component2Pin(Component): 
    
    def __init__(self, name, node1, node2, value, compType):
        super().__init__(name, value, compType, 2)
        super().addNode(node1)
        super().addNode(node2)


    # Measurement command for voltage 
    def createMeasCommandVol(self, measCommand):
        measText = ""
        
        if(self.nodes[1] == "0"): #if node is connected to ground
            measText = measText + measCommand % (self.name) + "(%s)\n" % (self.nodes[0])
        else:
            measText = measText + measCommand % (self.name) + "(%s,%s)\n" % (self.nodes[0], self.nodes[1])          
  
        return measText
    
    
    # Measurement command for current 
    def createMeasCommandCur(self, measCommand):
        measText = ""
        measText = measText + measCommand % (self.name) + "(%s)\n" % (self.name)
        
        return measText
    
    
    # Measurement command for power
    def createMeasCommandPow(self, measCommand):
        measText = ""
        
        if(self.nodes[1] == "0"): #if node is connected to ground
            measText = measText + measCommand % (self.name) + "(%s)*I(%s)\n" % (self.nodes[0], self.name)
        else:
            measText = measText + measCommand % (self.name) + "(%s,%s)*I(%s)\n" % (self.nodes[0], self.nodes[1], self.name)          
  
        return measText
    
    
    
class Component3Pin(Component):
    
    def __init__(self, name, node1, node2, node3, value, compType):
        super().__init__(name, value, compType, 3)
        super().addNode(node1)
        super().addNode(node2)
        super().addNode(node3)


    # Measurement command for voltage 
    def createMeasCommandVol(self, measCommand):
        measText = ""
        
        if(self.nodes[2] == "0"): #if node3 is connected to ground
            measText = measText + measCommand % (self.name + "+ce") + "(%s)\n" % (self.nodes[0])
            measText = measText + measCommand % (self.name + "+be") + "(%s)\n" % (self.nodes[1])            
        else:
            measText = measText + measCommand % (self.name + "+ce") \
                                + "(%s,%s)\n" % (self.nodes[0], self.nodes[2])          
            measText = measText + measCommand % (self.name + "+be") \
                                + "(%s,%s)\n" % (self.nodes[1], self.nodes[2])             
        return measText
    
    
    # Measurement command for current 
    def createMeasCommandCur(self, measCommand, prefix):
        measText = ""
        
        if(prefix == "Q"):
            measText = measText + measCommand % (self.name + "+c") + "c(%s)\n" % (self.name) #I collector
            measText = measText + measCommand % (self.name + "+b") + "b(%s)\n" % (self.name) #I base
            measText = measText + measCommand % (self.name + "+e") + "e(%s)\n" % (self.name) #I emitter                                
        if(prefix == "M"):
            measText = measText + measCommand % (self.name) + "(%s)\n" % (self.name)            

        return measText
    

        
class Resistor(Component2Pin):
    # numberOfMeas = 0
    def __init__(self, name, node1, node2, value):
        super().__init__(name, node1, node2, value, "resistor")



class Capacitor(Component2Pin):
    
     def __init__(self, name, node1, node2, value):
        super().__init__(name, node1, node2, value, "capacitor")

        

class Diode(Component2Pin):
    
     def __init__(self, name, node1, node2, model):
        super().__init__(name, node1, node2, model, "diode")
    
    

class BJT(Component3Pin):
    
    def __init__(self, name, node1, node2, node3, value):
        super().__init__(name, node1, node2, node3, value, "bjt")
