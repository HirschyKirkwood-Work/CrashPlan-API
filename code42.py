#!/usr/bin/env python3
from datetime import datetime
from helper import *

# TODO Users with no accounts (done)
# TODO users with accounts but no backups (done)
# TODO users with accounts and bad backups (done).
# TODO List all non-@andrew/alias emails (done).


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
                out_file, other=f"{member} does not have a CrashPlan account.\n"
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
                write_to_csv(out_file, member, users_machines)


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


def main():
    print(
        "Show users with no account based on grouper: 1\n"  # Prints info
        "Show users with an account but not a backup: 2\n"
        "Combine 1 and 2: 3\n"
        "Show users who don't have @andrew.cmu.edu: 4\no"
        "Show single user (only andrewID): 5"
    )
    answer: str = input("1/2/3/4/5: ")  # Gets user input
    start_time = (
        datetime.now()
    )  # Beginning of timing. Done here so reading options isn't counted in.
    if (
        answer == "1"
    ):  # Unforunately no *easy* way of not including the time taken choosing a file as it's not in this function.
        print("Checking for users with no account in CrashPlan")
        accountless()
    elif answer == "2":
        print("Checking for users without backups on record.")
        no_backup()
    elif answer == "3":
        print("Showing all users and their status.")
        full_report()
    elif answer == "4":
        print("Checking for accounts with aliases.")
        aliases()
    elif answer == "5":
        print("Get single user.")
        single_user: str = input("Enter AndrewID: ")
        get_single_user(single_user)
    else:
        print("Invalid option.")
    end_time = datetime.now()
    print(f"Duration: {end_time - start_time}")  # Prints time taken


if __name__ == "__main__":
    main()
