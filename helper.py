#!/usr/bin/env python3
import py42.sdk
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from dotenv import load_dotenv
import os
from pathlib import Path
import py42.sdk
import csv, re, shutil, tempfile

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
    # Device info dump
    # 'computerId': 21667277, 'name': 'CL-SGMARTIN-D',
    # 'osHostname': 'CL-SGMARTIN-D', 'guid': '962847553106330647',
    # 'type': 'COMPUTER', 'status': 'Active',
    # 'active': True, 'blocked': False,
    # 'alertState': 2, 'alertStates': ['CriticalConnectdeptnAlert'],
    # 'userId': 5665341, 'userUid': 'f6286ad2531aea56',
    # 'orgId': 537140, 'orgUid': 'ffdf5749-1d54-44e4-8f0e-da3c3c63e68e',
    # 'computerExtRef': None, 'notes': None,
    # 'parentComputerId': None,'parentComputerGuid': None,
    # 'lastConnected': '2022-02-16T18:33:39.479Z','osName': 'win64',
    # 'osVersdeptn': '10.0.19042','osArch': 'amd64',
    # 'address': 'REDACTED','remoteAddress': 'REDACTED',
    # 'javaVersdeptn': '', 'modelInfo': '',
    # 'timeZone': 'America/New_York',43'versdeptn': 1525200006882,
    # 'productVersdeptn': '8.8.2','buildVersdeptn': 143,
    # 'creatdeptnDate': '2020-07-13T10:14:14.594Z','modificatdeptnDate': '2022-10-13T16:14:02.734Z',
    # 'loginDate': '2022-02-16T15:13:59.460Z', 'service': 'CrashPlan'}

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
        print(
            f"User with UID {colored(255,0,0,UID)} does not have a machine associated with them.\n"
        )
        return f"User with UID {UID} does not have a machine associated with them.\n"
    return return_list


def get_single_user(andrewID):  # For one-off lookups.
    andrewID = f"{andrewID}@andrew.cmu.edu"
    cp_all_users = get_users()
    print(f"The Status of {andrewID} is:")
    return_value = user_machine_status(cp_all_users[andrewID])
    print(return_value)
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


def write_to_csv(file: str, andrewID: str = "", computers: list = [], other: str = ""):
    # print(f"Andrew: {andrewID} computers: {computers}, other: {other}")
    with open(file, "a") as f:
        if not andrewID:
            f.write(f"{other}\n")
        if andrewID:
            f.write(f"Username:,{andrewID}\n")
            for computer in computers:
                for key, value in computer.items():
                    f.write(f"Computer name:,{key}\n")
                    f.write(
                        f"Status:, {value['Status']},  Last_Modified:, {value['Last_Modified'][0:10]}\n"
                        f"Alert:, {value['Alert']}, OS:, {value['OS']}\n"
                    )


# write_to_csv("test", other="test,lol,good,one")
# write_to_csv("test", andrewID="hkirkwoo", computers=["this,", "that", "the other"])
