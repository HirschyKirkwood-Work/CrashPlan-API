#!/usr/bin/env python3
import py42.sdk
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from dotenv import load_dotenv
import os
from pathlib import Path
import py42.sdk
import csv, re, shutil, tempfile
from csv_to_html import HtmlConvert
from datetime import date

dotenv_path = Path("creds.env")
load_dotenv(dotenv_path=dotenv_path)  # Loads creds from a file in the .gitignore.
URL = "https://console.us2.crashplan.com/api/v3/auth/jwt?useBody=true"
UNAME = os.environ.get("username")
PWORD = os.environ.get("password")
SDK = py42.sdk.from_local_account(URL, UNAME, PWORD)  # Gets connection


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def flatten(l):  # Flattens out nexted list
    return [item for sublist in l for item in sublist]


def import_users(filename):
    with open(filename, newline="\n") as f:
        reader = csv.reader(f)
        dept = list(reader)
    dept = flatten(dept)
    return [f"{x}@andrew.cmu.edu" for x in dept]


def get_machines(UID):
    machine_response = SDK.devices.get_all(
        active=True, page_size=20000
    )  # Page size limits are stupid, but necessary, lol
    for page in machine_response:  # LOOOOOP
        devices = page["computers"]
        user_devices = {}  # Nested dict for user's devices
        for device in devices:
            # if 'OK' in str(device['alertStates']):
            #   continue
            if device["userUid"] == UID:
                user_devices[device["osHostname"]] = {
                    "Alert_State": device["alertStates"],
                    "Status": device["status"],
                    "UID": device["userUid"],
                    "Last_Modified": device["lastConnected"],
                    "Os_Type": device["osName"],
                }
                # return f"Hostname: {device['osHostname']}\nUserUID: {device['userUid']}\nOperating System: {device['osName']}\nAlert {device['alertStates']}\n"
            # if 'OK' not in str(device['alertStates']):
            # print(device['alertStates'])
            # return f"Hostname: {device['osHostname']}\nUserID: {device['userId']}\nOperating System: {device['osName']}\nAlert {device['alertStates']}\n"
        return user_devices


# {'userId': 28062831, 'userUid': '1060852660876723881', 'status': 'Active', 'username': 'alauth@andrew.cmu.edu',
#'email': 'alauth@andrew.cmu.edu', 'firstName': 'Aaron', 'lastName': 'Lauth', 'quotaInBytes': -1, 'orgId': 537140,
#'orgUid': 'ffdf5749-1d54-44e4-8f0e-da3c3c63e68e', 'orgGuid': '89muscpm892chp8c', 'orgName': 'Managed Hardware',
#'userExtRef': None, 'notes': None, 'active': True, 'blocked': False, 'invited': False, 'orgType': 'ENTERPRISE',
#'usernameIsAnEmail': True, 'creatdeptnDate': '2022-05-20T16:44:20.249Z', 'modificatdeptnDate': '2022-10-13T16:45:56.372Z',
#'passwordReset': False, 'localAuthenticatdeptnOnly': False, 'licenses': []}


def get_users():
    user_response = SDK.users.get_all(
        active=True
    )  # Could add page size here, but as of now, not required. Maybe DSP will get massive.
    all_users = {}  # Creates empty dict to store username and userUid pair to return
    for page in user_response:
        userz = page["users"]
        for user in userz:
            all_users[user["username"]] = user["userUid"]
    return all_users


def no_account(department, all_users):  # Gets list of users in dept w/o account
    return_val = []
    for member in department:
        if member not in all_users:
            return_val.append(member)
    return return_val


def file_dia(titl="Select a grouper file to check"):  # TK file dialog
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(
        title=titl
    )  # show an "Open" dialog box and return the path to the selected file
    return filename


def return_no_backup(users):  # Returns users with no backup
    return_value = []
    for user, UID in users.items():
        if len(get_machines(UID).items()) == 0:  # Count 0 lol
            return_value.append(user)
    return return_value


def return_dept_dict(
    cp_all, dept_all
):  # Returns dictionary with username/userUid combo for users w/ accounts in dept.
    no_acc = no_account(dept_all, cp_all)
    return_value = {}
    for member in dept_all:
        if member not in no_acc:
            return_value[member] = cp_all[member]
    return return_value


def user_machine_status(
    UID,
):  # I could probably integrate return_no_backup() with this. #TODO
    # print(f"Length: {len(get_machines(UID).items())}")
    machine_data = get_machines(UID)
    return_list = []
    if len(machine_data.items()) != 0:
        for key, value in machine_data.items():
            comp_dict = {}
            comp_dict[key] = {
                "Status": value["Status"],
                "Last_Modified": value["Last_Modified"][:10],
                "Alert": value["Alert_State"],
                "OS": {value["Os_Type"]},
            }
            return_list.append(comp_dict)
            # print(
            #     f"Computer name: {key}\n"
            #     f"Status: {value['Status']},  Last_Modified: {value['Last_Modified'][0:10]}\n"
            #     f"Alert: {value['Alert_State']}, OS: {value['Os_Type']}\n"
            # )
    else:
        var = colored(255, 0, 0, "NOT")
        print(f"""This user does {var} have a machine associated with them.\n""")
        return f"This user does not have a machine associated with them.,,,,"
    return return_list


def get_single_user(andrewID):  # For one-off lookups.
    andrewID = f"{andrewID}@andrew.cmu.edu"
    cp_all_users = get_users()
    print(f"The Status of {andrewID} is:")
    try:
        return_value = user_machine_status(cp_all_users[andrewID])
    except KeyError:
        print(f"{andrewID} Does not have a CrashPlan account.")
        exit(1)
    # print(r/seturn_value)
    for machine in return_value:
        for key, value in machine.items():
            print(f"Computer name: {colored(128,0,128,key)}")
            if "connection" in value["Alert"][0].lower():
                print(
                    # f"Computer name: {key}\n"
                    f"Status: {value['Status']},  Last_Modified: {colored(255,0,0,value['Last_Modified'][0:10])}\n"
                    f"Alert: {colored(255,0,0,value['Alert'])}, OS: {value['OS']}\n"
                )
            else:
                print(
                    # f"Computer name: {key}\n"
                    f"Status: {value['Status']},  Last_Modified: {colored(0,255,0,value['Last_Modified'][0:10])}\n"
                    f"Alert: {colored(0,255,0,value['Alert'])}, OS: {value['OS']}\n"
                )


def sed(
    file, pattern, repl
):  # Sed-like replace function. Thank you to David Miller on Stack Overflow https://stackoverflow.com/questions/4427542/how-to-do-sed-like-text-replace-with-python
    with open(
        file, "r"
    ) as sources:  # I think I've done similar stuff in the past with nested withs lol. I didn't realize your variables were accessible outside of the with.
        lines = sources.readlines()
    with open(file, "w") as sources:
        for line in lines:
            sources.write(re.sub(pattern, repl, line))


def clean_up(s: str):
    return_value = re.sub("[\[\]'\{\}]+", "", s)
    return_value = re.sub("OK", "Backing up", return_value)
    return_value = re.sub("CriticalConnectionAlert", "NOT backing up", return_value)
    return_value = return_value.rstrip()
    return return_value


def write_to_csv(file: str, andrewID: str = "", computers: list = [], other: str = ""):
    # print(f"Andrew: {andrewID} computers: {computers}, other: {other}")
    with open(file, "a") as f:
        if not andrewID:
            f.write(f"{other}\n")
        if andrewID:
            f.write(f"{andrewID},,,,,\n")
            for computer in computers:
                for key, value in computer.items():
                    f.write(
                        f",{key},"
                        f"{value['Status']},{value['Last_Modified'][0:10]},"
                        f"{value['Alert']},{value['OS']}\n"
                    )


def get_grouper():  # Recieves file from user, formats it as needed, get all CP users and returns values
    user_file: str = file_dia()
    sed(user_file, r"^\"ldap\",", "")
    sed(user_file, r"\"sourceId\",\"entityId\"\n", "")
    sed(user_file, r"^$", "")
    cp_all_users = get_users()
    dept_members = import_users(user_file)
    return user_file, cp_all_users, dept_members


def full_report():  # Rename eventually. This function returns the most info to user
    user_file, cp_all_users, dept_members = get_grouper()
    print(
        "Enter new file to write data to. Will be created in the .csv format. No Extension"
    )
    out_file: str = str(input("Enter File name: "))
    if not out_file.endswith(".csv"):
        out_file += ".csv"
    html_file = f"{out_file[:-4]}.html"
    t_user_file = re.search(r"(.*)/(.*)", user_file).group(2)
    write_to_csv(
        out_file,
        other=f"AndrewID,Computer Name,Status,Last Backup,Alert(s),Operating System",
    )
    no_acc = no_account(
        dept_members, cp_all_users
    )  # Almost removed this, but not using dept_dict()
    for (
        member
    ) in (
        dept_members
    ):  # here removes the functionality of showing users w/o accounts, lol
        if member in no_acc:
            print(
                f"{colored(255,0,0,member)} does {colored(255,0,0,'NOT')} have an CrashPlan account.\n"
            )
            write_to_csv(
                out_file, other=f"{member} does not have a CrashPlan account.,,,,,\n"
            )
            continue
        print(colored(255, 255, 0, member))
        users_machines = user_machine_status(
            cp_all_users[member]
        )  # Gets machine info for each machine associated with user.
        # print(users_machines)
        if isinstance(users_machines, str):  # User doesn't have backup
            write_to_csv(out_file, other=f"{member}, {users_machines}")
        else:
            for machine in users_machines:
                for key, value in machine.items():
                    for (
                        k,
                        v,
                    ) in value.items():
                        value[k] = clean_up(str(v))
                    print(f"Computer name: {colored(128,0,128,key)}")
                    if "not" in value["Alert"].lower():
                        print_value = f"Status: {value['Status']},  Last_Modified: {colored(255,0,0,value['Last_Modified'][0:10])}\nAlert: {colored(255,0,0,value['Alert'])}, OS: {value['OS']}\n"
                        print(clean_up(print_value))
                    else:
                        print(
                            # f"Computer name: {key}\n"
                            f"Status: {value['Status']},  Last_Modified: {colored(0,255,0,value['Last_Modified'][0:10])}\n"
                            f"Alert: {colored(0,255,0,value['Alert'])}, OS: {value['OS']}\n"
                        )
                write_to_csv(out_file, member, users_machines)
    xport = HtmlConvert(out_file, html_file)
    xport.main()


def parse_full(
    in_file: str, out_file: str
):  # Rename eventually. This function returns the most info to user
    cp_all_users = get_users()
    sed(in_file, r"^\"ldap\",", "")
    sed(in_file, r"\"sourceId\",\"entityId\"\n", "")
    sed(in_file, r"^$", "")
    dept_members = import_users(in_file)
    if not out_file.endswith(".csv"):
        out_file += ".csv"
    write_to_csv(
        out_file,
        other=f"AndrewID,Computer Name,Device Status,Last Backup, Backup Status,Operating System",
    )
    html_file = f"{out_file[:-4]}.html"
    no_acc = no_account(
        dept_members, cp_all_users
    )  # Almost removed this, but not using dept_dict()
    for (
        member
    ) in (
        dept_members
    ):  # here removes the functionality of showing users w/o accounts, lol
        if member in no_acc:
            print(
                f"{colored(255,0,0,member)} does {colored(255,0,0,'NOT')} have an CrashPlan account.\n"
            )
            write_to_csv(
                out_file, other=f"{member} does not have a CrashPlan account.,,,,,\n"
            )
            continue
        print(colored(255, 255, 0, member))
        users_machines = user_machine_status(
            cp_all_users[member]
        )  # Gets machine info for each machine associated with user.
        # print(users_machines)
        if isinstance(users_machines, str):  # User doesn't have backup
            write_to_csv(out_file, other=f"{member}, {users_machines}")
        else:
            for machine in users_machines:
                for key, value in machine.items():
                    for (
                        k,
                        v,
                    ) in value.items():
                        value[k] = clean_up(str(v))
                    print(f"Computer name: {colored(128,0,128,key)}")
                    if "not" in value["Alert"].lower():
                        print(
                            # f"Computer name: {key}\n"
                            f"Status: {value['Status']},  Last_Modified: {colored(255,0,0,value['Last_Modified'][0:10])}\n"
                            f"Alert: {colored(255,0,0,value['Alert'])}, OS: {value['OS']}\n"
                        )
                    else:
                        print(
                            f"Status: {value['Status']},  Last_Modified: {colored(0,255,0,value['Last_Modified'][0:10])}\nAlert: {colored(0,255,0,value['Alert'])}, OS: {value['OS']}\n"
                        )
            write_to_csv(out_file, member, users_machines)
    xport = HtmlConvert(out_file, html_file)
    xport.main()


def no_backup():  # Checks for users with no backups
    user_file, cp_all_users, dept_members = get_grouper()
    dept_dict: dict = return_dept_dict(
        cp_all_users, dept_members
    )  # Gets a dictionary of all users in Grouper that have an account.
    count: int = 0  # Count of users w/ no backup.
    for user in return_no_backup(dept_dict):
        print(colored(255, 0, 0, user))
        count += 1
    print(
        f"The number of users in this department without a backup is: {colored(255,0,0,count)}"
    )


def accountless():  # Gets All users with no account. Basically a wrapper function for no_account
    user_file, cp_all_users, dept_members = get_grouper()  # Gets necessary info
    no_acc = no_account(dept_members, cp_all_users)  # Gets users with no account
    for user in dept_members:
        if user in no_acc:
            print(f"No Account: {colored(255,0,0,user)}\n")


def aliases():  # Gets all users without @andrew
    cp_all_users = get_users()
    count = 0  # Count of Alias users
    for user in cp_all_users:
        if "andrew" not in user:  # Checks for Andrew
            print(user)
            count += 1
    print(
        f"The amount of all Managed Hardware users who have an alias is {colored(255,0,0,count)}\n"
        "This doesn't mean they don't have an actual email associated with their machines and should be checked manually."
    )


# write_to_csv("test", other="test,lol,good,one")
# write_to_csv("test", andrewID="hkirkwoo", computers=["this,", "that", "the other"])
