#!/usr/bin/env python3
import py42.sdk
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from dotenv import load_dotenv
import os
from pathlib import Path
import py42.sdk
import csv, re, shutil, tempfile


dotenv_path = Path('creds.env')
load_dotenv(dotenv_path=dotenv_path)
URL =  'https://console.us2.crashplan.com/api/v3/auth/jwt?useBody=true'
UNAME = os.environ.get('username')
PWORD =  os.environ.get('password')
SDK = py42.sdk.from_local_account(URL, UNAME, PWORD)


def flatten(l):
	return [item for sublist in l for item in sublist]

def import_users(filename):
	with open(filename, newline='\n') as f:
		reader = csv.reader(f)
		dept = list(reader)
	dept = flatten(dept)
	return [f"{x}@andrew.cmu.edu" for x in dept]

def get_machines(UID):
				#Device info dump
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

	machine_response = SDK.devices.get_all(active=True, page_size=20000)
	for page in machine_response:
	    devices = page["computers"]
	    user_devices = {}
	    for device in devices:
	    	# if 'OK' in str(device['alertStates']):
	    	# 	continue
	    	if device['userUid'] == UID:
	    		user_devices[device['osHostname']] = { 'Alert_State': device['alertStates'],'Status': device['status'],
	    		'UID': device['userUid'], 'Last_Modified': device['lastConnected'], 'Os_Type': device['osName']}
	    		# return f"Hostname: {device['osHostname']}\nUserUID: {device['userUid']}\nOperating System: {device['osName']}\nAlert {device['alertStates']}\n"
	    	#if 'OK' not in str(device['alertStates']):
	    		#print(device['alertStates'])
	    		#return f"Hostname: {device['osHostname']}\nUserID: {device['userId']}\nOperating System: {device['osName']}\nAlert {device['alertStates']}\n"
	    return user_devices


# {'userId': 28062831, 'userUid': '1060852660876723881', 'status': 'Active', 'username': 'alauth@andrew.cmu.edu', 
#'email': 'alauth@andrew.cmu.edu', 'firstName': 'Aaron', 'lastName': 'Lauth', 'quotaInBytes': -1, 'orgId': 537140, 
#'orgUid': 'ffdf5749-1d54-44e4-8f0e-da3c3c63e68e', 'orgGuid': '89muscpm892chp8c', 'orgName': 'Managed Hardware', 
#'userExtRef': None, 'notes': None, 'active': True, 'blocked': False, 'invited': False, 'orgType': 'ENTERPRISE', 
#'usernameIsAnEmail': True, 'creatdeptnDate': '2022-05-20T16:44:20.249Z', 'modificatdeptnDate': '2022-10-13T16:45:56.372Z', 
#'passwordReset': False, 'localAuthenticatdeptnOnly': False, 'licenses': []}

def get_users():
	user_response = SDK.users.get_all(active=True)
	all_users = {}
	for page in user_response:
		userz = page['users']
		for user in userz:
			all_users[user['username']] = user['userUid']
	return all_users

def no_account(department, all_users):
	return_val = []
	for member in department:
		if member not in all_users:
			return_val.append(member)
	return return_val

def file_dia():
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
	return filename

def return_no_backup(users):
	return_value = []
	for user,UID in users.items():
		if len(get_machines(UID).items()) == 0:
			return_value.append(user)
	return return_value

def return_dept_dict(cp_all, dept_all):
	no_acc = no_account(dept_all, cp_all)	
	return_value = {}
	for member in dept_all:
		if member not in no_acc:
			return_value[member] = cp_all[member]
	return return_value


def user_machine_status(UID):
	#print(f"Length: {len(get_machines(UID).items())}")
	machine_data = get_machines(UID)
	if len(machine_data.items()) != 0:
		for key,value in machine_data.items():
			print(f"Computer name: {key}\n"
				f"Status: {value['Status']},  Last_Modified: {value['Last_Modified'][0:10]}\n"
				f"Alert: {value['Alert_State']}, OS: {value['Os_Type']}\n")
	else:
		print(f"User with UID {UID} does not have a machine associated with them.\n")

def get_single_user(andrewID):
	andrewID = f"{andrewID}@andrew.cmu.edu"
	cp_all_users = get_users()
	print(f"The Status of {andrewID} is:")
	return_value = user_machine_status(cp_all_users[andrewID])

def sed(file, pattern, repl):
	with open(file, "r") as sources:
		lines = sources.readlines()
	with open(file, "w") as sources:
		for line in lines:
			sources.write(re.sub(pattern, repl, line))


