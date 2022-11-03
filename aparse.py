#!/usr/bin/env python3
import argparse
from helper import *

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-n",
    "--andrewID",
    required=False,
    help="AndrewID of the user. (For use with --single).",
)
ap.add_argument(
    "-o",
    "--out-file",
    required=False,
    help="Selects the output file (for use with --all",
)
ap.add_argument(
    "-i",
    "--in-file",
    required=False,
    help="Selects the grouper-generatd file (for use with --all).",
)
ap.add_argument(
    "-a",
    "--all",
    action="store_true",
    help="Runs the complete report. (provide -0/--out-file and -i/--in-file",
)
ap.add_argument(
    "-b",
    "--no-backup",
    action="store_true",
    help="Runs the no backup report. (no other flags needed)",
)
ap.add_argument(
    "-N",
    "--no-account",
    action="store_true",
    help="Runs the no account report. (no other flags needed)",
)
ap.add_argument(
    "-1",
    "--single",
    action="store_true",
    help="Looks up a single user. (Provide -n/--andrewID",
)
args = vars(ap.parse_args())

# display a friendly message to the user
# print(args['name'], args['path'])
def main():
    if args["single"]:
        get_single_user(args["andrewID"])
    elif args["all"]:
        if not args["in_file"]:
            print("Please include a file you wish to check.\n./aparse.py -h")
            exit(1)
        if not args["out_file"]:
            print("Please include a file you wish to output to.\n./aparse.py -h")
            exit(1)
        parse_full(args["in_file"], args["out_file"])
    elif args["no-backup"]:
        print("no-backup")
    elif args["no-account"]:
        print("no-account")
    else:
        print("Choose an option. --help")


main()
