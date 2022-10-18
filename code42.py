#!/usr/bin/env python3

from helper import *
#TODO Users with no accounts, users with accounts but no backups, users with accounts and bad backups.


def main():
	user_file = file_dia()
	sed_inplace(user_file, r'^\"ldap\",', '')
	sed_inplace(user_file, r'\"sourceId\",\"entityId\"\n', '')
	sed_inplace(user_file, r'^$', '')
	cp_all_users = get_users()
	dept_members = import_users(user_file)
	no_acc = no_account(dept_members, cp_all_users)
	for user in dept_members:
		print(user)
		if user in no_acc:
			print(f"No Account: {user}\n")
			continue
		current = cp_all_users[user]
		user_machine_status(current)
		print("\n")


if __name__ == '__main__':
	main()








