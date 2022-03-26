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

###################### Windows method ####################################################
def runWindows():
    print("win")
    command = "Get-Service | Export-Csv -Path ./service.csv"
    completed = subprocess.run(["powershell", "-Command", command], capture_output=True)
    if completed.returncode != 0:
        print("An error occured: %s", completed.stderr)
    else:
        print("csv successfully created / updated!")

####################### Linux method ####################################################
def runUbuntu():
    print("ub")
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

########################### o_s ########################################################
def o_s():
    if platform.system() == "Windows":
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

    for line in log_lines:
        if line[0].startswith("---"):

            date_0 = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", line[0]).span()[0]
            date_1 = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", line[0]).span()[1]
            date_from_log = line[0][date_0:date_1]

            hour_0 = re.search(r"[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", line[0]).span()[0]
            hour_1 = re.search(r"[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", line[0]).span()[1]
            hour_from_logs = line[0][hour_0:hour_1]

            date_0_to_check = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", date1).span()[0]
            date_1_to_check = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", date1).span()[1]
            date_to_check = date1[date_0_to_check:date_1_to_check]

            hour_0_to_check = re.search(r"[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", date1).span()[0]
            hour_1_to_check = re.search(r"[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", date1).span()[1]
            hour_to_check = date1[hour_0_to_check:hour_1_to_check]


            if date_from_log == date_to_check and hour_from_logs == hour_to_check:
                index1 = log_lines.index(line)
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
                for i in range(index2 + 1, len(log_lines)):
                    if not log_lines[i][0].startswith("---"):
                        service_and_status = log_lines[i][0].split(" ")
                        date2_log[service_and_status[0]] = service_and_status[1]
                    else:
                        break
    sample_diff(open(STATUS_LOG_FILE, "a"), date1_log, date2_log)

############################### main #########################################
if __name__ == '__main__':
    if (len(sys.argv) <= 1):
        raise "Mode was not selected Error!\n please choose: monitor or manual"

    # Monitor mode
    if ("monitor" == sys.argv[1]):
        if (len(sys.argv) <= 2):
            raise "Time not selected Error! please enter how much seconds to refresh monitor"

        # Get seconds
        seconds = sys.argv[2]
        str = "> Monitor mode: Refresh rate of {} seconds".format(seconds)
        print(str)


        while True:
            my_dict = sample(open(SERVICE_LIST_FILE, "a"))
            time.sleep(float(seconds))
            my_dict2 = sample(open(SERVICE_LIST_FILE, "a"))
            sample_diff(open(STATUS_LOG_FILE, "a"), my_dict, my_dict2)


    elif ("manual" == sys.argv[1]):
        print("> Manual mode")
        if (len(sys.argv) <= 5):
            raise "2 dates not selected Error! please enter 2 dates for sample range"

        txt_date1 = sys.argv[2] + " " + sys.argv[3]
        txt_date2 = sys.argv[4] + " " + sys.argv[5]

        filterByDates(txt_date1, txt_date2)

    else:
        raise "Use 'manual' or 'monitor' mode"
