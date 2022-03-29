# Service_Monitor

# About this project:
In this project I implemented a service monitor in Python. This tool
monitor the services running in the system, and report on changes that 
can be critical for us as SOC people.

# More about the project:
The tool support Windows and Linux – Ubuntu.
This tool has 2 modes:
Monitor: For X time that the user sets, the program samples every X 
time all the services running on the computer and shows whether a 
change is observed from the previous sample. Is there a service that is 
no longer running, or is there a service a new one is running in the 
system.
In this mode there are 2 relevant log files:
"service_list.log" - which will contain the titles of the time in which a 
sample was taken and below each title all the services and their status 
for that time sample.
"status_log.log" - This log file is for tracking purposes.
This file show the changes that occurred between samples for the 
changed services.
Manual: In this mode we will use the "service_list.log" file to load 2 
samples from different time frames and make a comparison. The 
program gets a date and time for 2 events, loads the 2 samples from the 
file, and displays changes like the monitor mode (A new process created 
in the more recent sample, a process that no longer runs in the more 
recent sample, etc.) All those changes will be written in "status_log.log"
file.

# Libraries Information:
Os- for operating system check if file exist, also for running ubuntu 
command for checking the services, and in order to see last modified of 
some files.
Platform- to check in which operating system to support.
Re- To find the dates and times in the relevant files (there was a use of 
date and time regex).
Sys- to use argv (input from terminal).
Datetime- for input user and record the date and time of each log.
Subprocess- for running windows command for checking the services.
Csv- to execute services to a csv file
Smtplib- connection with gmail.com to execute email hacker track 
information.

# Project structure:
The project has 2 main classes: "ServiceMonitor " , "Hacker_Identifier".
The first is the main program, it checking the relevant operating system, 
running the appropriate command to check services status and taking
samples according to user request (monitor or manual).
The last one purpose is to report about unwanted changes in the log 
files and send an alert email about it.
In fact, first of all we would like to run our tool at a given time in monitor 
mode to check what are the open servers and at any X time get a sample 
of the changes that have occurred.
After operating the tool in monitor mode we can run each time we want 
the tool in manual mode to get samples of the changes that have 
occurred between 2 different times.
Before activation of the tool, we can check that no change has been 
made to our log files by using "Hacker_Identifier".
We will run the "Hacker_Identifier" and it will check when the file was 
last updated and whether it was done through our tool or by malicious 
sabotage by someone else, and if so, we will receive an email 
notification about it!

# How to run the project:
Enter the project directory, open cmd (Windows) or terminal (Linux) 
through project's path and run the following command:
* python3 ServiceMonitor.py "monitor" "XXX" to run the project in 
monitor mode every XXX time.
OR
* python3 ServiceMonitor.py "manual" D1/M1/Y1 H1:M1:S1 D2/M2/Y2
H2:M2:S2 to run the project in manual mode between first and second 
dates

![image](https://user-images.githubusercontent.com/92723105/160689811-f6e9b6ae-2f1a-424e-a0eb-ab45912e346d.png)

![image](https://user-images.githubusercontent.com/92723105/160689837-2906b121-ec50-4f9b-88cc-01b913ff7730.png)

Then you will get those log files in your project directory:

![image](https://user-images.githubusercontent.com/92723105/160689919-778b198a-8c95-4272-8085-8bb3f575b9aa.png)
"services_list.log" 

![image](https://user-images.githubusercontent.com/92723105/160689968-68b13f06-429b-4015-b835-dedb070c91b3.png)
"status_log.log"

To run the "Hacker_Identifier" :

![image](https://user-images.githubusercontent.com/92723105/160690089-0faaa141-2024-475e-8980-c9464a2ab6ea.png)


Then you will see this in your terminal, if there was a malicious touch on 
the log files:

![image](https://user-images.githubusercontent.com/92723105/160690138-a5a5a1b7-bb05-45c6-8b74-b545f2deb0cf.png)


And you can go check your email box and see this message:

![image](https://user-images.githubusercontent.com/92723105/160690183-724d6b17-b590-45e4-9aee-0ec92d320e56.png)



