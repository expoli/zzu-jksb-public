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


def chrome_init():
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
    return browser


def sign_in(uid, pwd, user_email):
    formatted_uid = uid[-3:]

    browser = chrome_init()

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
        msg = "登陆中间出现异常（有人分布式拉了，我不说是谁）\n" + "用户：" + formatted_uid + " \n异常信息如下: \n" + e.__str__()

        # mail(msg, EMAIL_ADMIN)
        # mail(msg, user_email)

        return msg
    finally:
        # quit the browser
        print("Singing in for User {0} is finished".format(formatted_uid))
        browser.delete_all_cookies()
        browser.quit()
