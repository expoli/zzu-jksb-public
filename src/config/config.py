import os

USER_NAMES = []
USER_PWDS = []
USER_EMAILS = []
EMAIL_ADMIN = ""
EMAIL_SERVER = ""
EMAIL_USER = ""
EMAIL_PWD = ""


def spilt_env_to_list(env: str) -> list:
    env = os.getenv(env)
    if env != "":
        return env.split(',')
    else:
        return []


if len(USER_NAMES) == 0:

    # list
    USER_NAMES = spilt_env_to_list('USER_NAMES')
    USER_PWDS = spilt_env_to_list('USER_PWDS')
    USER_EMAILS = spilt_env_to_list('USER_EMAILS')

    # alone config
    EMAIL_ADMIN = os.getenv('EMAIL_ADMIN')
    EMAIL_SERVER = os.getenv('EMAIL_SERVER')
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PWD = os.getenv('EMAIL_PWD')

else:
    pass
