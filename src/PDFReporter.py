# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 13:41:49 2021

@author: Giray Balcı
"""

from fpdf import FPDF
from datetime import datetime #for pdf autotime stamp

class PDFReporter: 
    numberOfCOlumns = 8 #default
    
    def __init__(self, title, data, reportDate):
        self.title = title
        self.data = data
        self.reportDate = reportDate
        self.pdf = FPDF()
        self.pdf.set_font('Arial','',10.0) 

        # Effective page width, or just epw
        self.epw = self.pdf.w - 2*self.pdf.l_margin
    
        # Set column width to 1/4 of effective page width to distribute content 
        # evenly across table and page
        self.col_width = self.epw/self.numberOfCOlumns
        
        # Text height is the same as current font size
        self.th = self.pdf.font_size*1.4
        self.pdf.set_title(self.title)
  
        
    def __addCoverPage(self):
        self.pdf.add_page()
        # Remember to always put one of these at least once.
        
        self.pdf.set_font('Arial','B',20.0) 
        self.pdf.cell(self.epw, 0.0, self.title, align='C')
        self.pdf.ln(2*self.th)
        self.pdf.set_font('Arial','',10.0) 
        self.pdf.cell(self.epw, 0.0, "Report Date:  " + self.reportDate, align='C')

    
    def __addEndOfReport(self):
        # Print generation time on page
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        timeStamp = "Generated on: " + str(dt_string)
        
        self.pdf.ln(4*self.th)
        self.pdf.cell(self.epw, 0.0, timeStamp, align='R')        


    def __addDataTables(self):
    # Enter data in colums
    # Notice the use of the function str to coerce any input to the 
    # string type. This is needed
    # since pyFPDF expects a string, not a number.       
        
        self.pdf.add_page()
        
        header_names = ["Name",
                        "Value",
                        "Vrms",
                        "Vmax",
                        "Irms",
                        "Imax",
                        "Pavg",
                        "Pmax"]
       
        #test pagination. No real purpose
        for r in range(4):
            for comps in self.data:
                # Create table
                self.pdf.set_font('Arial','B',12.0)               
                self.pdf.cell(self.col_width*(comps[0].numberOfMeas+2), self.th, "%s Table"%  str.capitalize(comps[0].type), align='C', border=1)
                self.pdf.ln(self.th)     
                self.pdf.set_font('Arial','B',10.0) 
                
                for i in range(comps[0].numberOfMeas+2):
                    self.pdf.cell(self.col_width, self.th, header_names[i], border=1)
      
                self.pdf.ln(self.th)
                self.pdf.set_font('Arial','',10.0) 

                for c in comps:                     
                    self.pdf.cell(self.col_width, self.th, str(c.name), border=1)
                    self.pdf.cell(self.col_width, self.th, str(c.value), border=1)
    
                    try:
                        self.pdf.cell(self.col_width, self.th, str(c.vrms), border=1) 
                    except:
                        print("Variable %s has no measurement: VRMS" % c.name)
                    try:
                        self.pdf.cell(self.col_width, self.th, str(c.vmax), border=1) 
                    except:
                        print("Variable %s has no measurement: VMAX" % c.name)
                    try:
                        self.pdf.cell(self.col_width, self.th, str(c.irms), border=1) 
                    except:
                        print("Variable %s has no measurement: IRMS" % c.name)
                    try:
                        self.pdf.cell(self.col_width, self.th, str(c.imax), border=1) 
                    except:
                        print("Variable %s has no measurement: IMAX" % c.name)
                    try:
                        self.pdf.cell(self.col_width, self.th, str(c.pavg), border=1) 
                    except:
                        print("Variable %s has no measurement: PAVG" % c.name)
                    try:
                        self.pdf.cell(self.col_width, self.th, str(c.pmax), border=1) 
                    except:
                        print("Variable %s has no measurement: PMAX" % c.name)
    
                    self.pdf.ln(self.th)
                self.pdf.ln(self.th*2)      
        return 
 
        
    def setNumberOfColumns(self, numberOfCOlumns):
        self.numberOfCOlumns = numberOfCOlumns
        self.col_width = self.epw/self.numberOfCOlumns        
   

    # Create pdf file
    def export(self):        
        self.__addCoverPage()
        self.__addDataTables()        
        self.__addEndOfReport()
        
        self.pdf.output('Tutorial.pdf', 'F')

