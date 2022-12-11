import PySimpleGUI as sg
import csv
import sys
import threading
import datetime
import smtplib
import time
import os

# setting directories so script can be compiled into an executable and still find CSV
if getattr(sys, 'frozen', False):
    directory = os.path.dirname(sys.executable)
elif __file__:
    directory = os.path.dirname(__file__)

# constant definitions for email account information
SENDEREMAIL = ""
SENDERPASSWORD = ""
SMTPSERVER = ""

# function definitions which handle emailing based upon printer selection
# adding time.sleep() functions to seem more human
def ultimakerS3(emailAddress):
    smtpObj = smtplib.SMTP(SMTPSERVER, 587)
    smtpObj.ehlo()
    time.sleep(2)
    smtpObj.starttls()
    time.sleep(3)
    smtpObj.login(SENDEREMAIL, SENDERPASSWORD)
    time.sleep(4)
    smtpObj.sendmail(SENDEREMAIL, emailAddress, 'Subject: Your project has finished printing.\nYour project on the Ultimaker S3 has finished printing.')
    smtpObj.quit()

def ultimakerA(emailAddress):
    smtpObj = smtplib.SMTP(SMTPSERVER, 587)
    smtpObj.ehlo()
    time.sleep(2)
    smtpObj.starttls()
    time.sleep(3)
    smtpObj.login(SENDEREMAIL, SENDERPASSWORD)
    time.sleep(4)
    smtpObj.sendmail(SENDEREMAIL, emailAddress, 'Subject: Your project has finished printing.\nYour project on the Ultimaker A has finished printing.')
    smtpObj.quit()

def ultimakerB(emailAddress):
    smtpObj = smtplib.SMTP(SMTPSERVER, 587)
    smtpObj.ehlo()
    time.sleep(2)
    smtpObj.starttls()
    time.sleep(3)
    smtpObj.login(SENDEREMAIL, SENDERPASSWORD)
    time.sleep(4)
    smtpObj.sendmail(SENDEREMAIL, emailAddress, 'Subject: Your project has finished printing.\nYour project on the Ultimaker B has finished printing.')
    smtpObj.quit()

def ultimakerC(emailAddress):
    smtpObj = smtplib.SMTP(SMTPSERVER, 587)
    smtpObj.ehlo()
    time.sleep(2)
    smtpObj.starttls()
    time.sleep(3)
    smtpObj.login(SENDEREMAIL, SENDERPASSWORD)
    time.sleep(4)
    smtpObj.sendmail(SENDEREMAIL, emailAddress, 'Subject: Your project has finished printing.\nYour project on the Ultimaker C has finished printing.')
    smtpObj.quit()


# open csv with student emails to fill dropdown list in the GUI
try:
    with open(fr"{directory}\emails.csv", "r", encoding="utf-8-sig") as peopleFile:
        fileReader = csv.reader(peopleFile)
        peopleList = list(fileReader)
except:
    sg.popup("No email list file found. Please make a CSV with a list of emails in the first column and name the CSV emails.")
    sys.exit() #prevents the program from progressing if it can't find the necessary CSV

# make the GUI layout, which includes keys for specific printers
sg.theme("DarkBlack")

layout = [[sg.Text("Select your email address.")],
        [sg.Combo(peopleList, key="emailAddress", default_value="Please select your email.")],
        [sg.Text("Select your printer:")],
        [sg.Radio("Ultimaker S3", "RADIO1", key="ultS3", default=True), sg.Radio("Ultimaker A", "RADIO1", key="ultA"), sg.Radio("Ultimaker B", "RADIO1", key="ultB"), sg.Radio("Ultimaker C", "RADIO1", key="ultC")],
        [sg.Text("How long until your print is finished?")],
        [sg.Spin([i for i in range(0,100)], initial_value=0, key="projectHours"), sg.Text('Hours')], 
        [sg.Spin([i for i in range(1,60)], initial_value=0, key="projectMinutes"), sg.Text('Minutes')],
        [sg.Submit()]
]

window = sg.Window('Ultimaker Project Reminder', icon="clock.ico", size=(500,250)).Layout(layout)    

while True:                             
    event, values = window.read() 
    
    #assign values from GUI input's dictionary to variables
    receiverAddress = values["emailAddress"]
    projectHours = int(values["projectHours"]) #using int() to handle errors that turn 0 inputs into strings
    projectMinutes = int(values["projectMinutes"])
    totalProjectSeconds = (projectHours*3600) + (projectMinutes*60) #convert time input into seconds since that's what the Timer object takes as argument
    

    # main printing threads
    if event == "Submit":
        #create timestamp for each submission
        submitTime = datetime.datetime.now()
        submitTimeStamp = (fr"{submitTime.month}/{submitTime.day}/{submitTime.year} at {submitTime.hour}:{submitTime.minute}")

        # prevent large prints on smaller printers
        if not values["ultS3"] and projectHours >= 7:
            sg.popup("You cannot print a large project on the smaller printers. Please use the S3 if available.")
            continue
        
        #handle a blank email address
        if receiverAddress == "":
            sg.popup("Please enter a valid email address.")
            continue

        # handle accidentally entering 0 hours and 0 mins
        if totalProjectSeconds == 0:
            sg.popup("Please enter a time.")
            continue

        sg.popup(f"You will receive an email in {projectHours} hours and {projectMinutes} minutes when your project is completed.", icon="clock.ico")

        # append inputted information to CSV to create log of projects
        with open("projectlog.csv", "a", newline="") as fileLog:
            fileWriter = csv.writer(fileLog)
            fileWriter.writerow([receiverAddress[0], submitTimeStamp])

        # operation threads based upon printer choice. Uses functions defined above   
        if values["ultS3"]:
            thread1 = threading.Timer(totalProjectSeconds, ultimakerS3, receiverAddress)
            thread1.start()
        if values["ultA"]:
            thread2 = threading.Timer(totalProjectSeconds, ultimakerA, receiverAddress)
            thread2.start()
        if values["ultB"]:
            thread3 = threading.Timer(totalProjectSeconds, ultimakerB, receiverAddress)
            thread3.start()
        if values["ultC"]:
            thread4 = threading.Timer(totalProjectSeconds, ultimakerC, receiverAddress)
            thread4.start()
    
    if event == sg.WIN_CLOSED:
        thread1.quit()
        thread2.quit()
        thread3.quit()
        thread4.quit()
        break

window.close()
