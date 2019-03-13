'''
Author:         Austin Moore
Script Type:    Helper Script
Description:    This is a helper script to provide a function for logging into
                an OHIO account with Selenium
Python 3.7.2
'''

import re
import getpass
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

'''
Function:       ohio_login()
Arguments:      driver (Selenium driver)
Return Type:    void
Description:    Asks user for OHIO login ID and password. Completes the login
                by Selenium
'''
def ohio_login(driver):
    if (re.findall(r"login.microsoftonline.com", str(driver.current_url))):
        wait = WebDriverWait(driver, 10)

        print("\nPlease log in using the terminal\n")

        email = input("Enter OHIO email: ")
        password = getpass.getpass("Enter OHIO password: ")

        email_xpath = '//*[@id="i0116"]'
        password_xpath = '//*[@id="i0118"]'
        next_button_xpath = '//*[@id="idSIButton9"]'

        driver.find_element_by_xpath(email_xpath).send_keys(email)
        driver.find_element_by_xpath(next_button_xpath).click()

        driver.find_element_by_xpath(password_xpath).send_keys(password)
        wait.until(EC.presence_of_element_located((By.XPATH, next_button_xpath)))
        driver.find_element_by_xpath(next_button_xpath).click()
