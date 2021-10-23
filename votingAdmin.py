#imports
import tkinter as tk
import csvreader
import glob, os, shutil
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

#functions
def csvChoose():
    global sourcePath
    sourcePath = filedialog.askopenfilename()
    lblhold2.config(text = sourcePath)

def functionRun():
    strOutput = ""
    intLeading = 0
    strLeading = ''
    voteCounts = csvreader.run_Program(lblhold2['text'])
    strOutput += 'Pineapple Pizza Party' + ': ' + str(voteCounts['Pineapple Pizza Party']) + '\n'
    strOutput += 'Pronounced Jiff Union' + ': ' + str(voteCounts['Pronounced Jiff Union']) + '\n'
    strOutput += 'Socks and Crocs Reform League' + ': ' + str(voteCounts['Socks and Crocs Reform League'])
    for parties in voteCounts:
        if (voteCounts[parties]) > intLeading:
            intLeading = voteCounts[parties]
            strLeading = parties
    strOutput += '\nThe current leader is: ' + strLeading
    lblhold3.config(text = strOutput)

#global variables
global sourcePath

#tkinter GUI creation
root = tk.Tk()
root.title('Vote Ontario - Admin')

frmLeft = tk.Frame(master=root, relief = tk.RAISED)
frmLeft.grid(row=0,column=0)
btnChoose = tk.Button(frmLeft, text='CSV to Check', command = csvChoose, bg = "#425cc7", fg = 'white')
btnChoose.grid(row=0, column=0, pady = 10, sticky = 'NSEW')
btnVerify = tk.Button(frmLeft, text="Check CSV", command = functionRun, bg = "#425cc7", fg = 'white')
btnVerify.grid(row=1, column=0, pady = 10, sticky = 'NSEW')

frmRight = tk.Frame(master=root, relief = tk.SUNKEN)
frmRight.grid(row=0, column = 1)
lblhold2 = tk.Label(frmRight, text='Welcome to the Admin page for Vote Ontario.\n Use the left buttons to choose the voting CSV and then validate them', height=5)
lblhold2.grid(row=0, column=0, sticky = 'NSEW')
lblhold3 = tk.Label(frmRight, text='Voting results will appear here', height=5)
lblhold3.grid(row=1, column=0, sticky = 'NSEW')

root.mainloop()
