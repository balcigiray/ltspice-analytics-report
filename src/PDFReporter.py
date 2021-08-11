# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 13:41:49 2021

@author: Giray Balcı
"""

from fpdf import FPDF
from datetime import datetime #for pdf autotime stamp

class PDFReporter:
    prefix = {'y': 1e-24,  # yocto
            'z': 1e-21,  # zepto
            'a': 1e-18,  # atto
            'f': 1e-15,  # femto
            'p': 1e-12,  # pico
            'n': 1e-9,   # nano
            'u': 1e-6,   # micro
            'm': 1e-3,   # mili
            ' ': 1e-2,   # centi
            # 'd': 1e-1,   # deci
            'k': 1e3,    # kilo
            'M': 1e6,    # mega
            'G': 1e9,    # giga
            'T': 1e12,   # tera
            'P': 1e15,   # peta
            'E': 1e18,   # exa
            'Z': 1e21,   # zetta
            'Y': 1e24,   # yotta
    }   
    
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
        self.th = self.pdf.font_size*1.3
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
        
        
        
    def __getHeaderNames(self, component):
        header_names = ["NAME",
                        "VALUE"]
        
        if(component.numberOfNodes > 2):
            header_names.append("PARAM")
            
        meas = component.measurements
            
        for key in meas:
            results = meas[key]
            
            for key2 in results:
                if key2 not in header_names:
                    header_names.append(key2)
    
        return header_names
    
    
    
    def __numToReadable(self, number):
        strFormat = ">4.2f" #right aligned, 4 character width, 2 decimal points        
        readable = ""
        isNegative = None
        
        #check if number is negative
        if(number < 0):
            number *= -1
            isNegative = True

        for unit in self.prefix:
            if(number*1e-3 > self.prefix[unit]):
                continue   
            else:
               readable = format(number / self.prefix[unit], strFormat) + " " + unit
               break
           
        if(isNegative):
            readable = "-" + readable
       
        return readable
    
    

    def __addDataTables(self):
    # Enter data in colums
    # Notice the use of the function str to coerce any input to the 
    # string type. This is needed
    # since pyFPDF expects a string, not a number.       
        
        self.pdf.add_page()
        
        for comps in self.data:
            #Init header names
            headerNames = self.__getHeaderNames(comps[0])
            
            # Create table
            self.pdf.set_font('Arial','B',12.0)               
            
            # print table title
            self.pdf.cell(self.col_width*(len(headerNames)), self.th, "%s Table"%  str.capitalize(comps[0].compType), align='C', border=1)
            self.pdf.ln(self.th)     
            self.pdf.set_font('Arial','B',10.0)
            
            #print table headers
            for i in range(len(headerNames)):
                self.pdf.cell(self.col_width, self.th, headerNames[i].capitalize(), border=1)
  
            self.pdf.ln(self.th)
            self.pdf.set_font('Arial','',10.0)

            # fill in the table with data
            for c in comps:
                for key in c.measurements:
                    self.pdf.cell(self.col_width, self.th, str(c.name), border=1)
                    self.pdf.cell(self.col_width, self.th, str(c.value), border=1)

                    if(c.numberOfNodes > 2):
                        self.pdf.cell(self.col_width, self.th, key, border=1)
                    
                    results = c.measurements[key]
                    
                    addColumn = 0
                    
                    if(c.numberOfNodes > 2):
                        addColumn = 1
                        
                    for i in range(len(headerNames)-(2+addColumn)):
                        key = headerNames[i+2+addColumn]
                        try:
                            self.pdf.cell(self.col_width, self.th, self.__numToReadable(results[key]), border=1)
                        except:
                            self.pdf.cell(self.col_width, self.th, "*", border=1)
                        
                        
                    self.pdf.ln(self.th)
            self.pdf.ln(self.th*2)
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
