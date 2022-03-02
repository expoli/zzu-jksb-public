import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from src.config.config import *
from src.mail.mail import mail


def is_element_present(browser, xpath):
    from selenium.common.exceptions import NoSuchElementException

    try:
        element = browser.find_element_by_xpath(xpath)
    except NoSuchElementException as e:
        # print(e)
        return False
    else:
        return True


def sign_in(uid, pwd, user_email):
    formatted_uid = uid[-3:]

    # set to no-window
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ssl-version-fallback-min=tls1")

    # 0 - Default, 1 - Allow, 2 - Block
    # https://www.browserstack.com/docs/automate/selenium/handle-permission-pop-ups#handle-know-your-location-pop-up
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 2})

    # add acceptInsecureCerts
    capabilities = chrome_options.to_capabilities()
    capabilities['acceptInsecureCerts'] = True

    # simulate a browser to open the website
    browser = webdriver.Chrome(desired_capabilities=capabilities)
    # disable cache
    browser.delete_all_cookies()

    commit_msg = ""

    try:
        browser.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0")
        time.sleep(2)
        browser.get("https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0")

        # input uid and password
        print("Inputting the UID and Password of User {0}".format(formatted_uid))
        browser.find_element_by_xpath('//*[@id="mt_5"]/div[2]/div[3]/input').send_keys(uid)
        browser.find_element_by_xpath('//*[@id="mt_5"]/div[3]/div[3]/input').send_keys(pwd)

        # click to sign in
        browser.find_element_by_xpath('//*[@id="mt_5"]/div[5]/div/input').click()
        time.sleep(2)

        # get middle info
        real_mid_page_url = browser.find_element_by_xpath("//*[@id='zzj_top_6s']").get_attribute("src")
        browser.get(real_mid_page_url)
        time.sleep(2)

        # this day you
        # 今日您还没有填报过
        print("Checking whether User {0} has signed in".format(formatted_uid))
        if browser.find_element_by_xpath('//*[@id="bak_0"]/div[5]/span').text == '今日您已经填报过了':
            commit_msg += browser.find_element_by_xpath('//*[@id="bak_0"]/div[5]/span').text + '\n'
            return commit_msg

        # 点击开始本人填报
        # //*[@id="bak_0"]/div[11]/div[3]/div[4]/span
        browser.find_element_by_xpath('//*[@id="bak_0"]/div[11]/div[3]/div[4]/span').click()
        time.sleep(1)

        # 设置为绿码
        # //*[@id="bak_0"]/div[8]/div[2]/div[2]/div[2]/select[1]
        # //*[@id="bak_0"]/div[8]/div[2]/div[2]/div[2]/select[1]

        qr_status_sel = Select(browser.find_element_by_xpath('//*[@id="bak_0"]/div[8]/div[2]/div[2]/div[2]/select[1]'))
        qr_status_sel.select_by_value('g')

        # 设置疫苗接种情况为接种第三针
        # //*[@id="bak_0"]/div[8]/div[2]/div[2]/div[2]/div[2]/select

        qr_status_sel = Select(
            browser.find_element_by_xpath('//*[@id="bak_0"]/div[8]/div[2]/div[2]/div[2]/div[2]/select[1]'))
        qr_status_sel.select_by_value('5')

        # 点击提交表格

        # //*[@id="bak_0"]/div[8]/div[2]/div[2]/div[2]/div[6]/div[4]/span
        browser.find_element_by_xpath('//*[@id="bak_0"]/div[8]/div[2]/div[2]/div[2]/div[6]/div[4]/span').click()
        time.sleep(2)

        # 提交完成信息
        # //*[@id="bak_0"]/div[2]/div[2]/div[2]/div[2]
        commit_msg += browser.find_element_by_xpath('//*[@id="bak_0"]/div[2]/div[2]/div[2]/div[2]').text

        # 点击确认
        # //*[@id="bak_0"]/div[2]/div[2]/div[4]/div[2]
        browser.find_element_by_xpath('//*[@id="bak_0"]/div[2]/div[2]/div[4]/div[2]').click()
        time.sleep(2)

        # 最终完成信息
        # //*[@id="bak_0"]/div[2]
        commit_msg += browser.find_element_by_xpath('//*[@id="bak_0"]/div[2]').text + '\n'

        return commit_msg

    except Exception as e:
        msg = "while signing in for user " + formatted_uid + " there is an exception: \n" + e.__str__()
        # print(msg)
        mail(msg, EMAIL_ADMIN)
        mail(msg, user_email)
        return ""
    finally:
        # quit the browser
        print("Singing in for User {0} is finished".format(formatted_uid))
        browser.delete_all_cookies()
        browser.quit()


def timing(hour, minute, the_users):
    now = datetime.datetime.now()
    if now.hour == hour and now.minute == minute:
        print("\n\n\n")
        print(now)
        for user in the_users:
            formatted_uid = user.uid[-3:]
            commit_msg = sign_in(user.uid, user.pwd, user.email)

            msg = user.uid + ": " + commit_msg
            print("Emailing to User {0} for notification".format(formatted_uid))
            mail(msg, user.email)
            print("Emailing is finished")

# if __name__ == "__main__":

# For Single User
# msg = sign_in(UID, PWD)
# mail.mail(msg, EMAIL_TO)

# For Multiple Users
# for user in users:
#     msg = sign_in(user.uid, user.pwd)
#     print("Emailing to User {0} for notification".format(user.uid))
#     mail.mail(msg, user.email)
#     print("Emailing is finished")

# For Timing and Multiple Users
# while True:
#     # sign for tow
#     timing(6, 0, users)
#     # sign for the others
#     timing(8, 30, stus)
#
#     # sleep 30 secs
#     time.sleep(30)
