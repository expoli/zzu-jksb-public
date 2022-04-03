from src.core.core import *
from src.config.config import *
from src.user.user import User
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

users = []
# 尝试通过使用尝试次数增加容错率
retry_time = 10

while len(USER_NAMES) > 0:
    users.append(User(USER_NAMES.pop(), USER_PWDS.pop(), USER_EMAILS.pop()))

for user in users:
    done_flag = False
    for i in range(0, retry_time):
        try:
            # 进行登陆
            commit_msg = sign_in(user.uid, user.pwd, user.email)
            if "已完成今日" in commit_msg:
                msg = user.uid + ": " + commit_msg
                print("Emailing to User {0} for notification".format(user.uid[-3:]))
                mail(msg, user.email)
                print("Emailing is finished")
                done_flag = True
                break
            elif "今日您已经填报过了" in commit_msg:
                msg = user.uid + ": " + commit_msg
                print("Emailing to User {0} for notification".format(user.uid[-3:]))
                mail(msg, user.email)
                print("Emailing is finished")
                done_flag = True
                break
            elif i == retry_time - 1:
                msg = user.uid + ": " + commit_msg
                print("Emailing to User {0} for notification".format(user.uid[-3:]))
                # 出错信息提示
                mail(msg, user.email)
                mail(msg, EMAIL_ADMIN)
                print("Emailing is finished")
                break
        except Exception as e:
            print(e.__str__())
