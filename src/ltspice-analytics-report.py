# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 14:29:16 2021

@author: Giray Balcı
"""

# %%
# from fpdf import FPDF
import subprocess
import time 
import os
# from datetime import datetime #for pdf autotime stamp


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
from PDFReporter import PDFReporter

pr = PDFReporter(newName, results, "12.07.2021")
pr.export()

# DEBUG purposes
# automatically open, wait for visual inspection, close
DEBUG = True

if(DEBUG):
    subprocess.Popen(['Tutorial.pdf'], shell=True)
    time.sleep(10)
    os.system("taskkill /im " + "AcroRd32.exe" + " /F" )

