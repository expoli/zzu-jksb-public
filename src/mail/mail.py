import smtplib
from email.mime.text import MIMEText
from src.config.config import *


def mail(mail_text, mail_to):
    # set the mail context
    msg = MIMEText(mail_text)

    # set the mail info
    msg['Subject'] = "打卡邮件提醒"
    msg['From'] = EMAIL_USER
    msg['To'] = mail_to

    # send the mail
    send = smtplib.SMTP_SSL(EMAIL_SERVER, 465)
    send.login(EMAIL_USER, EMAIL_PWD)
    send.send_message(msg)
    # quit QQ EMail
    send.quit()
