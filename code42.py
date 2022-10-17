#!/usr/bin/env python3

from helper import *
#TODO Users with no accounts, users with accounts but no backups, users with accounts and bad backups.


def main():
	user_file = file_dia()
	cp_all_users = get_users()
	dept_members = import_users(user_file)
	no_acc = no_account(dept_members, cp_all_users)
	for user in dept_members:
		if user in no_acc:
			print(f"No Account: {user}")


if __name__ == '__main__':
	#main()
	for key,value in get_machines("f6286ad2531aea56").items():
		print(f"Computer name: {key}\n"
			f"Status: {value}\n")







