'''
Author:         Austin Moore
Script Type:    Helper Script
Description:    This is a helper script to provide a function for logging into
                an OHIO account with Selenium
'''

import re
from selenium import WebDriver

'''
Function:       ohio_login()
Return Type:    void
Description:    Asks user for OHIO login ID and password. Completes the login
                by Selenium
'''
def ohio_login():
    if (re.findall(r"cas.sso.ohio.edu", str(driver.current_url))):
        username = raw_input("Enter OHIO username: ")
        password = getpass.getpass("Enter OHIO password: ")

        element = driver.find_element_by_xpath(cas_username_xpath)
        element.send_keys(username)
        element = driver.find_element_by_xpath(cas_password_xpath)
        element.send_keys(password)
        element = driver.find_element_by_xpath(cas_login_button_xpath)
        element.click()
