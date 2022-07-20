import os 
import json
import sys

CHANGED_FILES = os.environ.get("CHANGED_FILES")
CURRENT_USER = os.environ.get("CURRENT_USER")
ALLOWED_USERS = os.environ.get("ALLOWED_USERS")

allowedUsersReadable = json.loads(ALLOWED_USERS)

#Der erste oberste Pfad wird als einzige gueltige Firma anerkannt
#Existiert diese nicht, oder aendert sie sich innerhalb eines Pull Requests, ist der Test ungueltig
currentCompany = CHANGED_FILES.split()[0].split('/')[0]

#Checken, ob in nur einem Pfad Aenderungen vorgenommen wurden
for file in CHANGED_FILES.split():
    if currentCompany == file.split('/')[0]:
        pass
    else:
        print("You are only allowed to make changes in one directory!")
        sys.exit(1)

#Checken ob CURRENT_USER für currentCompany zugelassen ist
try:
    for i in range(len(allowedUsersReadable)):
        if allowedUsersReadable[i][currentCompany]:
            for user in allowedUsersReadable[i][currentCompany]:
                if user == CURRENT_USER:
                    print("User is valid!")
                    sys.exit(0)
                    
except (KeyError):
    print("You are not allowed, to make changes in this directory!")
    sys.exit(1) 
