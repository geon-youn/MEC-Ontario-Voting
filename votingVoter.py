import cv2
import pytesseract
import tkinter as tk
import glob, os, shutil
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from datetime import datetime
import backend
import csv

choiceVote = ''

def changeTime():
    now-datetime.now()
    current_time = now.strftime("%H:%M")
    lblTime.config(text='Current Time is: ' + current_time)

def imageChoose():
    global sourcePath
    sourcePath = filedialog.askopenfilename()
    lblhold2.config(text='Uploaded')
    changeTime

def validate():
    global sourcePath
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    idText = (pytesseract.image_to_string(sourcePath)).lower()
    last_name = (entLast.get()).lower()
    first_name = (entFirst.get()).lower()
    global votes
    with open('votingList.csv') as csvfile:
        votes ={}
        entries = csv.reader(csvfile)
        # add valid entries to the dictionary
        for entry in entries:
            # create full name of voter
            name = " ".join(entry[0:2])
            # get the party the person voted for
            party = entry[2]
            # add vote to dictionary if the vote is valid
            if name not in votes and party in {'Pineapple Pizza Party', 'Pronounced Jiff Union', 'Socks and Crocs Reform League'}:
                votes[name] = party
    if first_name in idText and last_name in idText:
        lblhold3.config(text = 'Authenticated, proceeding to vote')
        votingScreen(votes)
        lblWelcome.config(text='You have been validated.')
    else:
        lblhold3.config(text = 'ERROR: ID not recognized or does not match. Please try again.')
        return
    changeTime
                                  
def votingScreen(votes):
    lblhold2.destroy()
    lblhold3.destroy()
    frmRight.destroy()
    btnOne = tk.Button(frmLeft, text='Vote', command = buttonOne)
    btnTwo = tk.Button(frmLeft, text='Vote', command = buttonTwo)
    btnThree = tk.Button(frmLeft, text='Vote', command = buttonThree)
    btnOne.grid(row=0, column=0, sticky = 'NSEW')
    btnTwo.grid(row=1, column=0, sticky = 'NSEW')
    btnThree.grid(row=2, column=0, sticky = 'NSEW')
    lblOne = tk.Label(frmLeft, text = 'Pineapple Pizza Party')
    lblTwo = tk.Label(frmLeft, text = 'Pronounced Jiff Union')
    lblThree = tk.Label(frmLeft, text = 'Socks and Crocs Reform League')
    lblOne.grid(row=0, column= 1, sticky = 'NSEW')
    lblTwo.grid(row=1, column= 1, sticky = 'NSEW')
    lblThree.grid(row=2, column= 1, sticky = 'NSEW')
    btnSubmit2 = tk.Button(frmLeft, text= 'Submit Vote', command = finalVote, bg = "#425cc7", fg = 'white')
    btnSubmit2.grid(row=3, column=1, sticky = 'NSEW')
    changeTime
    
def buttonOne():
    global choiceVote
    choiceVote = 'Pineapple Pizza Party'
    lblTime.config(text='Submitted: Pineapple Pizza Party',bg = "#425cc7", fg = 'white')
    
def buttonTwo():
    global choiceVote
    choiceVote = 'Pronounced Jiff Union'
    lblTime.config(text='Submitted: Pronounced Jiff Union',bg = "#425cc7", fg = 'white')
def buttonThree():
    global choiceVote
    choiceVote = 'Socks and Crocs Reform League'
    lblTime.config(text='Submitted: Socks and Crocs Reform League',bg = "#425cc7", fg = 'white')

def finalVote():
    global votes
    last_name = entLast.get()
    first_name = entFirst.get()
    name = first_name +' '+last_name
    if(backend.auth_vote(name, choiceVote, votes)):
        lblWelcome.config(text='Vote Submitted')        
        name = first_name.capitalize() +' '+last_name.capitalize()
        votes[name] = choiceVote
        backend.save_csv_file(votes)
    else:
        lblWelcome.config(text='You have already voted. \nVoter fraud a crime, the police have been notified and are en route')
        lblWelcome.config(bg = 'red')
    changeTime
    
Font_tuple = ("Comic Sans MS", 20, "bold") 
root = tk.Tk()
root.title('Vote Ontario - Voter')
lblWelcome = tk.Label(root, text = 'Welcome to Vote Ontario! Please Enter Your Last Name and First Name to be authenticated')
lblWelcome.grid(row=0, column=0)
now = datetime.now()
current_time = now.strftime("%H:%M")
lblTime = tk.Label(root, text = '     Current Time is: ' + current_time)
lblTime.grid(row=0, column=1)

frmLeft = tk.Frame(master=root, relief = tk.RAISED)
frmLeft.grid(row=1,column=0)
lblLast = tk.Label(frmLeft, text="Last Name:")
lblLast.grid(row=0, column=0, pady = 5, sticky = 'NSEW')
lblFirst = tk.Label(frmLeft, text='First Name:')
lblFirst.grid(row=0, column=1, pady = 5, padx = 3, sticky = "NSEW")
entLast = tk.Entry(frmLeft)
entLast.grid(row=1, column=0, pady = 5, padx = 3, sticky = 'NSEW')
entFirst=tk.Entry(frmLeft)
entFirst.grid(row=1, column=1, pady = 5, padx = 3, sticky = 'NSEW')

btnChoose = tk.Button(frmLeft, text='Select ID Picture', bg = "#425cc7", fg = 'white', command = imageChoose)
btnChoose.grid(row=2, column=0, pady = 5, padx = 3, sticky = 'NSEW')
btnSubmit = tk.Button(frmLeft, text='Press to Authenticate (results on the right)',bg = "#425cc7", fg = 'white', command = validate)
btnSubmit.grid(row=2, column=1, pady = 5, padx = 3, sticky = 'NSEW')

frmRight = tk.Frame(master=root, relief = tk.SUNKEN)
frmRight.grid(row=1, column = 1)
lblhold2 = tk.Label(frmRight, text='Loading...', height=5)
lblhold2.grid(row=0, column=0, sticky = 'NSEW')
lblhold3 = tk.Label(frmRight, text='', height=5)
lblhold3.grid(row=1, column=0, sticky = 'NSEW')

root.mainloop()
