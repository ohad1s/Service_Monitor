import os
import platform
import re
import sys
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
    o_s()
    open_ser_csv = open("service.csv", encoding="utf8")
    read_ser_csv = reader(open_ser_csv)
    services_data = list(read_ser_csv)
    date_ = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write("---------------------" + date_ + "--------------------------\n")
    for i in range(2, len(services_data) - 1):
        service_name = services_data[i][8]
        service_status = services_data[i][11]
        line_to_write = "{} {}\n".format(service_name, service_status)
        log_file.write(line_to_write)
        # log_file.write("\n")
        dict[service_name] = service_status
    log_file.close()
    return dict


############################# sample_diff ########################################

def sample_diff(log_file, sample1, sample2):
    for service_, status_ in sample1.items():
        date = datetime.now()
        if service_ not in sample2:
            str = "Service {} is found at sample 1 but not sample 2. This service probably was uninstalled".format(
                service_)
            print(str)
            log_file.write(str + "\n")
        elif status_ != sample2[service_]:
            str = "{}: Service '{}' changed status from '{}' to '{}'".format(date, service_, status_, sample2[service_])
            print(str)
            log_file.write(str + "\n")


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
    if platform == "Windows":
        runWindows()
    else:
        runUbuntu()


########################### filter with 2 dates ######################################################
def filterByDates(date1, date2):
    date1_log = {}
    date2_log = {}
    log_file = open(SERVICE_LIST_FILE, "r")
    read_log_file = reader(log_file)
    log_lines = list(read_log_file)
    # print(log_lines)

    for line in log_lines:
        if line[0].startswith("---"):

            date_0 = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", line[0]).span()[0]
            date_1 = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", line[0]).span()[1]
            date_from_log = line[0][date_0:date_1]

            hour_0 = re.search(r"[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", line[0]).span()[0]
            hour_1 = re.search(r"[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", line[0]).span()[1]
            hour_from_logs = line[0][hour_0:hour_1]

            # hour_from_logs = re.search(r"[\d]{1,2}:[\d]{1,2}:[\d]{1,2}",line[0])
            # match = re.search(r"\s(\d{2}\:\d{2}\",line)

            date_0_to_check = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", date1).span()[0]
            date_1_to_check = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", date1).span()[1]
            date_to_check = date1[date_0_to_check:date_1_to_check]


            hour_0_to_check = re.search(r"[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", date1).span()[0]
            hour_1_to_check = re.search(r"[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", date1).span()[1]
            hour_to_check = date1[hour_0_to_check:hour_1_to_check]

            print(date_from_log)
            print(date_to_check)
            print(hour_from_logs)
            print(hour_to_check)
            if date_from_log == date_to_check and hour_from_logs == hour_to_check:
                print("yes")
                index1 = log_lines.index(line)
                print(index1)
                for i in range(index1 + 1, len(log_lines)):
                    if not log_lines[i][0].startswith("---"):
                        service_and_status = log_lines[i][0].split(" ")
                        date1_log[service_and_status[0]] = service_and_status[1]
                    else:
                        break

            date_0_to_check2 = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", date2).span()[0]
            date_1_to_check2 = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", date2).span()[1]
            date_to_check2 = date2[date_0_to_check2:date_1_to_check2]


            hour_0_to_check2 = re.search(r"[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", date2).span()[0]
            hour_1_to_check2 = re.search(r"[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", date2).span()[1]
            hour_to_check2 = date2[hour_0_to_check2:hour_1_to_check2]

            if date_from_log == date_to_check2 and hour_from_logs == hour_to_check2:
                index2 = log_lines.index(line)
                print(index2)
                for i in range(index2 + 1, len(log_lines)):
                    if not log_lines[i][0].startswith("---"):
                        service_and_status = log_lines[i][0].split(" ")
                        date2_log[service_and_status[0]] = service_and_status[1]
                    else:
                        break
    sample_diff(open(STATUS_LOG_FILE, "a"), date1_log, date2_log)

    #


# for line in log_file:
# 	str_line_date = line[0:19]
# 	line_date = validDate(str_line_date)
# 	if line_date == False:
# 		print("> Something went wront with date conversion of status log")
# 		exit()
# 	if date1 <= line_date <= date2:
# 		result.append(line)
# return result

############################### main #########################################
if __name__ == '__main__':
    if (len(sys.argv) <= 1):
        raise "Mode was not selected Error!\n please choose: monitor or manual"
        # print("Choose mode: monitor or manual")
        # exit()
    # Monitor mode
    if ("monitor" == sys.argv[1]):
        if (len(sys.argv) <= 2):
            raise "Time not selected Error! please enter how much seconds to refresh monitor"
            # print("Enter how much seconds to refresh monitor")
            # exit()
        # Get seconds
        seconds = sys.argv[2]
        str = "> Monitor mode: Refresh rate of {} seconds".format(seconds)
        print(str)

        platform = platform.system()
        # status_log = open(STATUS_LOG_FILE, "a")
        # log_file = open(SERVICE_LIST_FILE, "a")
        #
        #
        # dict = sample(log_file)
        while True:
            my_dict = sample(open(SERVICE_LIST_FILE, "a"))
            time.sleep(float(seconds))
            my_dict2 = sample(open(SERVICE_LIST_FILE, "a"))
            sample_diff(open(STATUS_LOG_FILE, "a"), my_dict, my_dict2)


    elif ("manual" == sys.argv[1]):
        print("> Manual mode")
        if (len(sys.argv) <= 5):
            raise "2 dates not selected Error! please enter 2 dates for sample range"
            # print("Please enter 2 dates for sample range")
            # exit()
        txt_date1 = sys.argv[2] + " " + sys.argv[3]
        txt_date2 = sys.argv[4] + " " + sys.argv[5]
        # mipo:
        # date1 = validDate(txt_date1)
        # date2 = validDate(txt_date2)
        # if date1 == False or date2 == False:
        #      raise "Please try again"
        #     # exit()
        # adpo
        # Success, now search the correct sampleings
        # filterByDates(date1, date2) kolel
        filterByDates(txt_date1, txt_date2)
        # print("> Total events found: " + str(len(lines)))
        # for line in lines:
        #     print(line)
    else:
        raise "Use 'manual' or 'monitor' mode"
        # exit()

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
