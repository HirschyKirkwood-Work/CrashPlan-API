#!/usr/bin/env python3
from datetime import datetime
from helper import *
from csv_to_html import HtmlConvert

# TODO Users with no accounts (done)
# TODO users with accounts but no backups (done)
# TODO users with accounts and bad backups (done).
# TODO List all non-@andrew/alias emails (done).


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
