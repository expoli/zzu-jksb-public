from src.core.core import *
from src.config.config import *
from src.user.user import User
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

users = []

try:

    while len(USER_NAMES) > 0:
        users.append(User(USER_NAMES.pop(), USER_PWDS.pop(), USER_EMAILS.pop()))

    # For Timing and Multiple Users
    # while True:
    #     # sign for tow
    #     timing(8, 0, users)
    #     # sign for the others
    #     # timing(8, 30, stus)
    #
    #     # sleep 30 secs
    #     time.sleep(30)
    for user in users:
        commit_msg = sign_in(user.uid, user.pwd, user.email)
        if commit_msg != "":
            msg = user.uid + ": " + commit_msg
            print("Emailing to User {0} for notification".format(user.uid[-3:]))
            mail(msg, user.email)
            print("Emailing is finished")

except Exception as e:
    print(e.__str__())
    exit(1)
