'''
Author:         Austin Moore
Script Type:    Helper Script
Description:    This is a helper script to provide a function for logging into
                an OHIO account with Selenium
'''

import re
import getpass
from selenium import webdriver

'''
Function:       ohio_login()
Arguments:      driver (Selenium driver)
Return Type:    void
Description:    Asks user for OHIO login ID and password. Completes the login
                by Selenium
'''
def ohio_login(driver):
    print

    cas_username_xpath = "//*[@id='username']"
    cas_password_xpath = "//*[@id='password']"
    cas_login_button_xpath = "/html/body/div[1]/div[2]/div/form/section[3]/div/button[1]"

    login_complete = False

    if (re.findall(r"cas.sso.ohio.edu", str(driver.current_url))):
        username = raw_input("Enter OHIO username: ")
        password = getpass.getpass("Enter OHIO password: ")

        element = driver.find_element_by_xpath(cas_username_xpath)
        element.send_keys(username)
        element = driver.find_element_by_xpath(cas_password_xpath)
        element.send_keys(password)
        element = driver.find_element_by_xpath(cas_login_button_xpath)
        element.click()
