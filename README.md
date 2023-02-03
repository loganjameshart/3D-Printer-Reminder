# Ultimaker Reminder

![tool](https://user-images.githubusercontent.com/116290186/205368526-b3dad036-3a9d-4a68-9e1b-2f158196cd2f.PNG)

## Overview

This is program that will automatically send an email when a student's project has finished printing.
It pulls the list of students' email addresses from a local CSV so that updating the yearly list is as simple as overwriting the old CSV.
It also appends a CSV file everytime a project is submitted to create a running log of projects inputted.

## How it works

After a student selects their printer and inputs the time remaining in their print, a new Threading Timer object is created. This Thread targets a function which emails the student when the print is finished.

Because of the multiple threads, this program is able to handle notifying users of multiple printers.

## Outside Libraries (can be installed with pip)

PySimpleGUI (https://pypi.org/project/PySimpleGUI/)
