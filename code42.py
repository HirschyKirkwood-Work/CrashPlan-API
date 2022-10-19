#!/usr/bin/env python3

from helper import *
#TODO Users with no accounts (done)
#TODO users with accounts but no backups (done)
#TODO users with accounts and bad backups (done).
#TODO List all non-@andrew/alias emails

def get_grouper():
	user_file = file_dia()
	sed_inplace(user_file, r'^\"ldap\",', '')
	sed_inplace(user_file, r'\"sourceId\",\"entityId\"\n', '')
	sed_inplace(user_file, r'^$', '')
	cp_all_users = get_users()
	dept_members = import_users(user_file)
	return user_file, cp_all_users, dept_members

def main():
	user_file, cp_all_users, dept_members  = get_grouper()
	no_acc = no_account(dept_members, cp_all_users)
	for user in dept_members:
		print(user)
		if user in no_acc:
			print(f"No Account: {user}\n")
			continue
		current = cp_all_users[user]
		user_machine_status(current)
		print("\n")

def no_backup():
	user_file, cp_all_users, dept_members  = get_grouper()
	dept_dict = return_dept_dict(cp_all_users, dept_members)
	for user in return_no_backup(dept_dict):
		print(user)
	# for member in dept_members:
	# 	if member not in no_acc:
			
	# # for user in dept_members:
	# 	no_acc = no_account(dept_members, cp_all_users)
	# 	if user in no_acc:
	# 		continue
	# 	current = cp_all_users[user]
	# 	user_machine_status(current, no_machine=True, usr=user)
	# 	print("\n")

def accountless():
	user_file, cp_all_users, dept_members = get_grouper()
	no_acc = no_account(dept_members, cp_all_users)
	for user in dept_members:
		if user in no_acc:
			print(f"No Account: {user}\n")


def aliases():
	cp_all_users = get_users()
	count = 0
	for user in cp_all_users:
		if "andrew" not in user:
			print(user)
			count += 1
	print(f"The amount of all Managed Hardware users who have an alias is {count}\n"
		"This doesn't mean they don't have an actual email associated with their machines and should be checked manually.")

if __name__ == '__main__':
	print("Show users with no account based on grouper: 1\n"
		"Show users with an account by not backup: 2\n"
		"Combine 1 and 2: 3\n"
		"Show users who don't have @andrew.cmu.edu: 4\no")
	answer = input("1/2/3/4: ")
	if answer == "1":
		print("Checking for users with no account in CrashPlan")
		accountless()
	elif answer == "2":
		print("Running option 2")
		no_backup()
	elif answer == "3":
		print("Running option 3.")
		main()
	elif answer == "4":
		print("Running option 4")
		aliases()
	else:
		print("Invalid option.")
	# accountless()
	# no_backup()
	# main()
	# aliases()







