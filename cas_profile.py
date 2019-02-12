'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    This script migrates profile pages to Ohio University Drupal
                pages
'''

import re
import time
import io
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ohio_login import ohio_login
from drupal_image import *

def script_main(driver, url, pos):
    page_source = driver.page_source
    page_source = page_source.replace(u"\xa0", u" ")
    page_source = page_source.replace(u"\xc2", u" ")
    soup = BeautifulSoup(page_source, features="html.parser")

    display_name = soup.find("h1", class_="fullProfileName").text

    full_name = display_name.split()
    first_name = full_name[0]
    last_name = full_name[len(full_name) - 1]

    try:
        title = soup.find("h3", class_="cas_Title").text
    except:
        pass

    try:
        department = "-" + soup.find("span", class_="cas_Department").text
    except:
        pass

    email = soup.find("span", class_="cas_Email").text
    ohio_id = re.findall("(.*?)@ohio.edu", email)[0]

    try:
        phone = soup.find("span", class_="cas_Phone").text
    except:
        pass

    profile_page_url = "https://webcmsstage.oit.ohio.edu/cas/group/1/content/create/group_node%3Astaff_profile"

    print("display_name = " + display_name)
    print("first_name = " + first_name)
    print("last_name = " + last_name)
    print("title = " + title)
    print("department = " + department)
    print("email = " + email)
    print("ohio_id = " + ohio_id)
    print("phone = " + phone)

    driver.get(profile_page_url)
    ohio_login(driver)
    wait = WebDriverWait(driver, 10)

    display_name_xpath = '//*[@id="edit-title-0-value"]'
    first_name_xpath = '//*[@id="edit-field-first-name-0-value"]'
    last_name_xpath = '//*[@id="edit-field-last-name-0-value"]'
    image_xpath = '//*[@id="edit-field-image-0-upload"]'
    alt_text_xpath = '//*[contains(@id, "edit-field-image-0-alt")]'
    title_xpath = '//*[@id="edit-field-title-0-value"]'
    department_xpath = '//*[@id="edit-field-department"]'
    profile_type_xpath = '//*[@id="edit-field-profile-type"]'
    ohio_id_xpath = '//*[@id="edit-field-ohio-id-0-value"]'
    email_xpath = '//*[@id="edit-field-email-0-value"]'
    phone_xpath = '//*[@id="edit-field-phone-0-value"]'
    save_xpath = '//*[@id="edit-submit"]'

    driver.find_element_by_xpath(display_name_xpath).send_keys(display_name)
    driver.find_element_by_xpath(first_name_xpath).send_keys(first_name)
    driver.find_element_by_xpath(last_name_xpath).send_keys(last_name)

    try:
        driver.find_element_by_xpath(title_xpath).send_keys(title)
    except:
        pass

    try:
        Select(driver.find_element_by_xpath(department_xpath).select_by_text(department))
    except:
        pass

    '''
    profile = "Faculty"
    Select(driver.find_element_by_xpath(profile_type_xpath).select_by_text(profile))
    '''

    driver.find_element_by_xpath(ohio_id_xpath).send_keys(ohio_id)
    driver.find_element_by_xpath(email_xpath).send_keys(email)

    try:
        driver.find_element_by_xpath(phone_xpath).send_keys(phone)
    except:
        pass

    try:
        file_name, image_title, alt_text = download_image(url, soup.find("div", class_="fullProfileImg"))
        driver.find_element_by_xpath(image_xpath).send_keys(os.getcwd() + "/images/" + file_name)
        wait.until(EC.presence_of_element_located((By.XPATH, alt_text_xpath)))
        driver.find_element_by_xpath(alt_text_xpath).send_keys(alt_text)
    except:
        pass


    driver.find_element_by_xpath(save_xpath).click()

    # Accept alert
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

