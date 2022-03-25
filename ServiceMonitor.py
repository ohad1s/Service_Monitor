import os
import platform
import sys
import threading
from _datetime import datetime
import time
import subprocess
from csv import reader

SERVICE_LIST_FILE = "service_list.log"
STATUS_LOG_FILE = "status_log.log"
SERVICES_LIST_BY_TIME = {}


####################### Windows method ####################################################
def runWindows():
    command = "Get-Service | Export-Csv -Path ./service.csv"
    completed = subprocess.run(["powershell", "-Command", command], capture_output=True)
    if completed.returncode != 0:
        print("An error occured: %s", completed.stderr)
    else:
        print("csv successfully created / updated!")


####################### Linux method ####################################################
def runUbuntu():
    os.system("systemctl list-units --type=service |awk '{print $1,$4}' | sed -E 's/ +/,/g' > service.csv")

############################# sample ########################################
def sample(log_file):
    dict = {}
    date = datetime.datetime.now()
    log_file.write("{}\n".format(date))
    o_s()
    open_ser_csv = open("service.csv", encoding="utf8")
    read_ser_csv = reader(open_ser_csv)
    services_data = list(read_ser_csv)
    log_file.write("---------------------"+str(datetime.now())+"--------------------------\n")
    for i in range(2, len(services_data) - 1):
        service_name = services_data[i][8]
        service_status = services_data[i][11]
        line_to_write = "{} {}\n".format(service_name, service_status)
        log_file.write(line_to_write)
        log_file.write("\n")
        dict[service_name]=service_status
    log_file.close()
    return dict

############################# sample_diff ########################################

def sample_diff(log_file,sample1,sample2):
    for service_, status_ in sample1.items():
        date = datetime.datetime.now()
        if service_ not in sample2:
            str = "Service {} is found at sample 1 but not sample 2. This service probably was uninstalled".format(service_)
            print(str)
            log_file.write(str + "\n")
            # log_file.flush()
        elif status_ != sample2[service_]:
            str = "{}: Service '{}' changed status from '{}' to '{}'".format(date, service_, status_, sample2[service_])
            print(str)
            log_file.write(str + "\n")
            # log_file.flush()


# ############################ monitor ###########################################
# def monitor(sec):
#     # o_s()
#     # open_ser_csv = open("service.csv", encoding="utf8")
#     # read_ser_csv = reader(open_ser_csv)
#     # services_data = list(read_ser_csv)
#     fp_service_list = open(SERVICE_LIST_FILE, "a", encoding="utf8")
#     fp_service_list.write("Service Name:\t\t Status:\n")
#     services_dict1 = {}
#     services_dict2 = {}
#     dict_flag = 1
#     fp_status_log = open(STATUS_LOG_FILE, "a", encoding="utf8")
#     print("bdika1")
#     fp_status_log.write("Status log file:\n")
#     # +str(datetime.now()) + "\n"
#     print("bdika2")
#
#     while (1):
#
#         # for i in range(2, len(services_data) - 1):
#         #     fp_service_list.write(
#         #         services_data[i][8] + "\t-\t" + services_data[i][11] + "\t-\t" + str(datetime.now()) + "\n")
#         # fp_service_list.write("-----------------------------------------------------------------\n")
#         if dict_flag == 1:
#             for i in range(2, len(services_data) - 1):
#                 services_dict1[services_data[i][8]] = services_data[i][11]
#             SERVICES_LIST_BY_TIME[str((str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(
#                 datetime.now().day) + "-" + str(datetime.now().hour)
#                                        + ":" + str(datetime.now().minute) + ":" + str(
#                         datetime.now().second)))] = services_dict1
#             if len(services_dict2.keys()) > 0:
#                 for s in services_dict1.keys():
#                     if s in services_dict2.keys():
#                         if services_dict1[s] != services_dict2[s]:
#                             fp_status_log.write(s + "\t\t" + services_dict1[s] + "\t\t" + str(datetime.now()) + "\n")
#                     else:
#                         fp_status_log.write(s + "\t\t" + services_dict1[s] + "\t\t" + str(datetime.now()) + "\n")
#             dict_flag = 2
#         else:
#             for i in range(2, len(services_data) - 1):
#                 services_dict2[services_data[i][8]] = services_data[i][11]
#             SERVICES_LIST_BY_TIME[str((str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(
#                 datetime.now().day) + "-" + str(datetime.now().hour)
#                                        + ":" + str(datetime.now().minute) + ":" + str(
#                         datetime.now().second)))] = services_dict2
#             for s in services_dict2.keys():
#                 if s in services_dict1.keys():
#                     if services_dict2[s] != services_dict1[s]:
#                         fp_status_log.write(s + "\t\t" + services_dict2[s] + "\t\t" + str(datetime.now()) + "\n")
#                 else:
#                     fp_status_log.write(s + "\t\t" + services_dict2[s] + "\t\t" + str(datetime.now()) + "\n")
#             dict_flag = 1
#
#         time.sleep(sec)
#         o_s()
#         open_ser_csv.close()
#         open_ser_csv = open("service.csv", encoding="utf8")
#         read_ser_csv = reader(open_ser_csv)
#         services_data = list(read_ser_csv)


############################ manual ###########################################
# def manual(time1, time2):
#     services_dict_time1 = SERVICES_LIST_BY_TIME[time1]
#     services_dict_time2 = SERVICES_LIST_BY_TIME[time2]
#     fp_status_log = open(STATUS_LOG_FILE, "a", encoding="utf8")
#     fp_status_log.write("Status log file:" + str(datetime.now()) + "\n")
#     fp_status_log.write("difference between:" + time1 + " to " + time2)
#     for s in services_dict_time2.keys():
#         if s in services_dict_time1.keys():
#             if services_dict_time2[s] != services_dict_time1[s]:
#                 fp_status_log.write(s + "\t\t" + services_dict_time2[s] + "\t\t" + str(datetime.now()) + "\n")
#         else:
#             fp_status_log.write(s + "\t\t" + services_dict_time2[s] + "\t\t" + str(datetime.now()) + "\n")
#     print("Comparison finished and sent to status log file!")


########################### o_s ########################################################
def o_s():
    if platform.system() == "Windows":
        runWindows()
    else:
        runUbuntu()

############################### main #########################################
if __name__ == '__main__':
    if (len(sys.argv) <= 1):
        raise "Mode was not selected Error!\n please choose: monitor or manual"
        # print("Choose mode: monitor or manual")
        # exit()
    # Monitor mode
    if ("monitor" == sys.argv[1]):
        if (len(sys.argv) <= 2):
            raise "Time not selected Error!\n please enter how much seconds to refresh monitor"
            # print("Enter how much seconds to refresh monitor")
            # exit()
        # Get seconds
        seconds = sys.argv[2]
        str = "> Monitor mode: Refresh rate of {} seconds".format(seconds)
        print(str)

        initFiles()
        platform = platform.system()
        status_log = open(STATUS_LOG_FILE, "a")
        log_file = open(SERVICE_LIST_FILE, "a")
        ###################################### Windows Platform ######################################
        if (platform == "Windows"):
            print("> Windows detected")
            dict = Win_SampleToLog(log_file)
            while True:
                my_dict = Win_SampleToLog(open(SERVICE_LIST_FILE, "a"))
                time.sleep(float(seconds))
                my_dict2 = Win_SampleToLog(open(SERVICE_LIST_FILE, "a"))
                DiffSamples(status_log, my_dict, my_dict2, platform)



        ###################################### Linux Platform ######################################
        else:
            print("> Linux detected")
            dict = Linux_SampleToLog(log_file)
            while True:
                my_dict = Linux_SampleToLog(open(SERVICE_LIST_FILE, "a"))
                time.sleep(float(seconds))
                my_dict2 = Linux_SampleToLog(open(SERVICE_LIST_FILE, "a"))
                DiffSamples(status_log, my_dict, my_dict2, platform)

    elif ("manual" == sys.argv[1]):
        print("> Manual mode")
        if (len(sys.argv) <= 5):
            print("Please enter 2 dates for sample range")
            exit()
        txt_date1 = sys.argv[2] + " " + sys.argv[3]
        txt_date2 = sys.argv[4] + " " + sys.argv[5]

        date1 = validDate(txt_date1)
        date2 = validDate(txt_date2)
        if date1 == False or date2 == False:
            print("Please try again")
            exit()

        # Success, now search the correct sampleings
        lines = filterStatusLogByDates(date1, date2)
        print("> Total events found: " + str(len(lines)))
        for line in lines:
            print(line)

    else:
        print("Use 'manual' or 'monitor' mode")
        exit()



    # time_for_monitor = int(input("How often do you want the monitor to work?  (in SECONDS)"))
    # print("service monitor is working...")
    # monitor_thread = threading.Thread(target=monitor, args=(time_for_monitor,))
    # monitor_thread.setDaemon(True)
    # monitor_thread.start()
    # WORK = True
    # while (WORK):
    #     print("loop:", WORK)
    #     what_to_do_flag = input("Would you like to stop the monitor? Press 0\n"
    #                             "Would you like to take a manual sample? Press 1\n"
    #                             "else press 2\n")
    #     if what_to_do_flag == 0:
    #         print(what_to_do_flag, "   what_flag")
    #         WORK = False
    #         print(WORK)
    #         print(what_to_do_flag, "   what_flag hahahahah worked")
    #     elif what_to_do_flag == 1:
    #         print(what_to_do_flag, "   what_flag")
    #         time1 = input("enter first time (YYYY/MM/DD-HH:MM:SS format)")
    #         time2 = input("enter second time (YYYY/MM/DD-HH:MM:SS format)")
    #         print(what_to_do_flag, "   what_flag hahahahah worked")
    #         manual_thread = threading.Thread(target=manual, args=(time1, time2,))
    #         manual_thread.start()
    #     else:
    #         print(what_to_do_flag, "   what_flag")
    #         time.sleep(10)
    # monitor(2)

    # manual("2022/03/24-21:10:28","2022/03/24-21:10:50")
