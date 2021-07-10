# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 14:29:16 2021

@author: Giray Balcı
"""

# %%
from fpdf import FPDF
import subprocess
import time 
import os
from datetime import datetime #for pdf autotime stamp


fileName = "exampleCircuit.asc"
dir_XVIIx64 = "C:\Program Files\LTC\LTspiceXVII\\"
exeName = "XVIIx64.exe"


# %%
from SpiceHandler import SpiceHandler

sh = SpiceHandler(dir_XVIIx64, exeName, fileName)

myList = sh.getComponentList()

# %%
meas = sh.generateMeasCommand()
newName = sh.createNewSimFile(meas)
sh.runSimulation(newName)

# %%
results = sh.getSimulationResults()



# %%
# once PDF generation section is mature, put below code into a class.

pdf = FPDF()
pdf.add_page()
# Remember to always put one of these at least once.
pdf.set_font('Times','',10.0) 

# Effective page width, or just epw
epw = pdf.w - 2*pdf.l_margin

# Set column width to 1/4 of effective page width to distribute content 
# evenly across table and page
col_width = epw/6

# Document title centered, 'B'old, 14 pt
pdf.set_font('Arial','B',14.0) 
pdf.cell(epw, 0.0, 'Circuit Analysis Report', align='C')
pdf.set_font('Arial','',10.0) 
pdf.ln(0.5)

# Text height is the same as current font size
th = pdf.font_size*1.4

pdf.ln(2*th)
pdf.cell(epw, 0.0, 'Using: ' + fileName, align='C')

pdf.ln(5*th)

# Create table
pdf.set_font('Arial','B',10.0) 
pdf.cell(col_width, th, "Name", border=1)
pdf.cell(col_width, th, "Value", border=1)
pdf.cell(col_width, th, "Vrms", border=1)
pdf.cell(col_width, th, "Vmax", border=1)
pdf.ln(th)
pdf.set_font('Arial','',10.0) 

# Enter data in colums
# Notice the use of the function str to coerce any input to the 
# string type. This is needed
# since pyFPDF expects a string, not a number.
for comps in myList:
    for c in comps:
            pdf.cell(col_width, th, str(c.name), border=1)
            pdf.cell(col_width, th, str(c.value), border=1)
            pdf.cell(col_width, th, str(c.vrms), border=1) 
            pdf.cell(col_width, th, str(c.vmax), border=1)             
            pdf.ln(th)
    
# Print generation time on page
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
timeStamp = "Generated on: " + str(dt_string)

pdf.ln(4*th)
pdf.cell(epw, 0.0, timeStamp, align='R')
    
# Generate pdf file
pdf.output('Tutorial.pdf', 'F')


# DEBUG purposes
# automatically open, wait for visual inspection, close
DEBUG = True

if(DEBUG):
    subprocess.Popen(['Tutorial.pdf'], shell=True)
    time.sleep(10)
    os.system("taskkill /im " + "AcroRd32.exe" + " /F" )

# %%   

