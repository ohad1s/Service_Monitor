import datetime
import os
import smtplib

SERVICE_LIST_FILE = "service_list.log"
STATUS_LOG_FILE = "status_log.log"
TIMESTMPS_LIST_FILE= "time_stmp_list.log"
TIMESTMPS_DIFF_FILE= "time_stmp_diff.log"

# ############################## email sending ################################
def Email_Sending():
    TO = 'shirazi1997@gmail.com'
    SUBJECT = 'Hacker_Identifier!'
    TEXT = "someone change things in your services list log or in status log !!!"
    gmail_sender = 'goat123messi@gmail.com'
    gmail_passwd = 'tuvsahrzh'
    print("Connecting to server...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    print("Server connected.")
    server.ehlo()
    server.starttls()
    print("Login to email...")
    server.login(gmail_sender, gmail_passwd)
    print("Logged in.")
    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print('email sent successfully.')
    except:
        print('error sending mail')

    server.quit()

# ######################## Hacker Identifier #################################
def Hacker_Identifier():
    fp1=open(TIMESTMPS_LIST_FILE,"r")
    fp2=open(TIMESTMPS_DIFF_FILE,"r")
    last_modif_list=os.path.getmtime(SERVICE_LIST_FILE)
    last_modif_diff=os.path.getmtime(STATUS_LOG_FILE)
    for line in fp1:
        date_=datetime.datetime.strptime(line,"%m/%d/%Y %H:%M:%S")
        print(date_)
        print(datetime.datetime.fromtimestamp(last_modif_list))
        if date_ > datetime.datetime.fromtimestamp(last_modif_list):
            Email_Sending()
    for line in fp2:
        date_=datetime.datetime.strptime(line,"%m/%d/%Y %H:%M:%S")
        if date_ > datetime.datetime.fromtimestamp(last_modif_diff):
            Email_Sending()

Hacker_Identifier()

if __name__ == '__main__':
    Hacker_Identifier()