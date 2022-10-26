# To Install:
```
git clone git@github.com:HirschyKirkwood-Work/CrashPlan-API.git
cd CrashPlan-API
```
# Install Requirements
`pip3 install -r requirements.txt`

On Mac, I had to use brew to `brew install python-tk` to get the dep to work even though pip does have a package シ 

# Usage

`./code42.py`

You will be greeted with an input prompt:

```
Show users with no account based on grouper: 1
Show users with an account but not a backup: 2
Combine 1 and 2: 3
Show users who don't have @andrew.cmu.edu: 4
o
1/2/3/4: 
```
Choosing options 1-3 will spawn a file dialog box. Select a csv file generated with the "lite" option generated from Grouper.

## Option 1:
This option will show you all users from Grouper that don't have a Crashplan account.

Example:
```
Checking for users with no account in CrashPlan
No Account: dwhowell@andrew.cmu.edu

Duration: 0:00:05.091949
```
## Option 2:
Shows users with no backup on record.

Example
```
Checking for users without backups on record.
⬛⬛⬛@andrew.cmu.edu
⬛⬛@andrew.cmu.edu
⬛⬛⬛@andrew.cmu.edu
The number of users in this department without a backup is: 3
Duration: 0:00:08.427012
```
## Option 3:
This is simply a combination of options 1 and 2. Without the count of each.

Example:
```
Showing all users and their status.
⬛⬛⬛@andrew.cmu.edu
User with UID ⬛⬛⬛⬛⬛ does not have a machine associated with them.

⬛⬛⬛@andrew.cmu.edu does not have an CrashPlan account.

⬛@andrew.cmu.edu
Computer name: ⬛⬛⬛
Status: Active,  Last_Modified: 2022-10-19
Alert: ['OK'], OS: win64

⬛⬛⬛@andrew.cmu.edu
User with UID ⬛⬛⬛⬛⬛ does not have a machine associated with them.

Duration: 0:00:06.953113
```
## Option 4:
Shows all account created with an email alias (not @andrew.cmu.edu)

Example:
```
...
The amount of all Managed Hardware users who have an alias is 72
This doesn't mean they don't have an actual email associated with their machines and should be checked manually.
Duration: 0:00:01.799781
```
