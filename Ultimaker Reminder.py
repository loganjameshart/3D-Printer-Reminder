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

#constant definitions for email account information
SENDEREMAIL = "crb3dprinters@gmail.com"
SENDERPASSWORD = "acvrabukrrvyprwg"
SMTPSERVER = "smtp.gmail.com"

# email function

def send_email(email_address, printer_name=None):
    smtpObj = smtplib.SMTP(SMTPSERVER, 587)
    smtpObj.ehlo()
    time.sleep(2)
    smtpObj.starttls()
    time.sleep(3)
    smtpObj.login(SENDEREMAIL, SENDERPASSWORD)
    time.sleep(4)
    smtpObj.sendmail(SENDEREMAIL, email_address, f'Subject: Your project has finished printing.\nYour project on the {printer_name} has finished printing.')
    smtpObj.quit()

# function definitions which handle emailing based upon printer selection (thread Timer objects need functions as targets)

def ultimakerS3(email_address):
    send_email(email_address, "Ultimaker S3")

def ultimakerA(email_address):
    send_email(email_address, "Ultimaker A")

def ultimakerB(email_address):
    send_email(email_address, "Ultimaker B")

def ultimakerC(email_address):
    send_email(email_address, "Ultimaker C")

def enderA(email_address):
    send_email(email_address, "Ender A")

def enderB(email_address):
    send_email(email_address, "Ender B")

def enderC(email_address):
    send_email(email_address, "Ender C")

# open csv with student emails to fill dropdown list in the GUI

try:
    with open(fr"{directory}\emails.csv", "r", encoding="utf-8-sig") as people_file:
        file_reader_object = csv.reader(people_file)
        people_list = list(file_reader_object)
except:
    sg.popup("No email list file found. Please make a CSV with a list of emails in the first column and name the CSV emails.")
    sys.exit() #prevents the program from progressing if it can't find the necessary CSV

# make the GUI layout, which includes keys for specific printers

sg.theme("DarkBlack")

layout = [[(sg.Text("Logan's Cool-ass Ulitmaker Reminder Program", font=("Roboto", 22))), (sg.Push()), sg.Image(fr"{directory}\hearthart.png", size=(100,100))],
        [sg.Text("Select your email address.", font=("Arial", 18))],
        [sg.Combo(people_list, key="email_address", default_value="Please select your email.", font=('Arial', 16))],
        [sg.Text('')], # blank text box used as spacer
        [sg.Text("Select your printer:", font=("Arial", 16))],
        [sg.Radio("Ultimaker S3", "RADIO1", key="ultS3", default=True, font=('Arial', 14)), sg.Radio("Ultimaker A", "RADIO1", key="ultA", font=('Arial', 14)), 
        sg.Radio("Ultimaker B", "RADIO1", key="ultB", font=('Arial', 14)), sg.Radio("Ultimaker C", "RADIO1", key="ultC", font=('Arial', 14)),
        sg.Radio("Ender A", "RADIO1", key="enderA", font=('Arial', 14)), sg.Radio("Ender B", "RADIO1", key="enderB", font=('Arial', 14)), 
        sg.Radio("Ender C", "RADIO1", key="enderC", font=('Arial', 14))],
        [sg.Text('')],
        [sg.Text("How long until your print is finished?", font=('Arial', 14))],
        [sg.Spin([i for i in range(0,100)], initial_value=0, key="project_hours", font=('Arial', 14)), sg.Text('Hours', font=('Arial', 14))], 
        [sg.Spin([i for i in range(1,60)], initial_value=0, key="project_minutes", font=('Arial', 14)), sg.Text('Minutes', font=('Arial', 14))],
        [sg.Text('')],
        [sg.Submit()]
]

window = sg.Window('Ultimaker Project Reminder', icon="clock.ico", size=(1000,500)).Layout(layout)    


# Main program loop #

while True:                             
    event, values = window.read() 
    
    if event == sg.WIN_CLOSED:
        sys.exit()
    
    #assign values from GUI input's dictionary to variables
    receiver_address = values["email_address"]
    project_hours = int(values["project_hours"]) #using int() to handle errors that turn 0 inputs into strings
    project_minutes = int(values["project_minutes"])
    total_project_seconds = (project_hours*3600) + (project_minutes*60) #convert time input into seconds since that's what the Timer object takes as argument
    
    # main printing threads
    if event == "Submit":
        #create timestamp for each submission
        submitTime = datetime.datetime.now()
        submitTimeStamp = (fr"{submitTime.month}/{submitTime.day}/{submitTime.year} at {submitTime.hour}:{submitTime.minute}")

        # prevent large prints on smaller printers
        if not values["ultS3"] and project_hours >= 7:
            sg.popup("You cannot print a large project on the smaller printers. Please use the S3 if available.")
            continue
        
        #handle a blank email address
        if receiver_address == "":
            sg.popup("Please select a valid email address. If you can't find your name, please contact Matt.")
            continue

        # handle accidentally entering 0 hours and 0 mins
        if total_project_seconds == 0:
            sg.popup("Please enter a time.")
            continue


        sg.popup(f"You will receive an email in {project_hours} hours and {project_minutes} minutes when your project is completed.", icon="clock.ico")

        # append inputted information to CSV to create log of projects
        with open("projectlog.csv", "a", newline="") as fileLog:
            fileWriter = csv.writer(fileLog)
            fileWriter.writerow([receiver_address[0], submitTimeStamp])

        # operation threads based upon printer choice. Uses functions defined above   
        if values["ultS3"]:
            thread1 = threading.Timer(total_project_seconds, ultimakerS3, receiver_address)
            thread1.start()
        if values["ultA"]:
            thread2 = threading.Timer(total_project_seconds, ultimakerA, receiver_address)
            thread2.start()
        if values["ultB"]:
            thread3 = threading.Timer(total_project_seconds, ultimakerB, receiver_address)
            thread3.start()
        if values["ultC"]:
            thread4 = threading.Timer(total_project_seconds, ultimakerC, receiver_address)
            thread4.start()
        if values["enderA"]:
            thread5 = threading.Timer(total_project_seconds, enderA, receiver_address)
            thread5.start()
        if values["enderB"]:
            thread6 = threading.Timer(total_project_seconds, enderB, receiver_address)
            thread6.start()
        if values["enderC"]:
            thread7 = threading.Timer(total_project_seconds, enderC, receiver_address)
            thread7.start()
    
    if event == sg.WIN_CLOSED:
        thread1.cancel()
        thread2.cancel()
        thread3.cancel()
        thread4.cancel()
        thread5.cancel()
        thread6.cancel()
        thread7.cancel()
        sys.exit()
