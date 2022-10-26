#!/usr/bin/env python3
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True, help="name of the user")
ap.add_argument("-p", "--path", required=True, help="full path of the grouper file")
args = vars(ap.parse_args())

# display a friendly message to the user
# print(args['name'], args['path'])
print(f"Hi there {args['name']}, it's nice to meet you! The path you selected is {args['path']}")