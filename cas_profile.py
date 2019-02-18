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
from fix_html import *

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

    if (re.findall(r"-Biological Sciences", department)):
        department = "-Biology"
    if (re.findall(r"-Biological Sciences Emeriti", department)):
        department = "-Biology"
    if (re.findall(r"-Center for Law, Justice & Culture", department)):
        department = "-Law Center"
    if (re.findall(r"-Chemistry & Biochemistry", department)):
        department = "-Chemistry"
    if (re.findall(r"-Chemistry & Biochemistry Emeriti", department)):
        department = "-Chemistry"
    if (re.findall(r"-Classics & World Religions", department)):
        department = "-Classics"
    if (re.findall(r"-Contemporary History Institute", department)):
        department = "-Contemporary History"
    if (re.findall(r"-Dean's Office", department)):
        department = "-Dean"
    if (re.findall(r"-Economics Emeritus", department)):
        department = "-Economics"
    if (re.findall(r"-Environmental & Plant Biology", department)):
        department = "-Plant Biology"
    if (re.findall(r"-Environmental & Plant Biology Emeritus", department)):
        department = "-Plant Biology"
    if (re.findall(r"-Geological Sciences", department)):
        department = "-Geology"
    if (re.findall(r"-History Emeriti", department)):
        department = "-History"
    if (re.findall(r"-Mathematics", department)):
        department = "-Math"
    if (re.findall(r"-Philosophy Emeritus", department)):
        department = "-Philosophy"
    if (re.findall(r"-Physics & Astronomy", department)):
        department = "-Physics and Astronomy"
    if (re.findall(r"-Physics & Astronomy Emeriti", department)):
        department = "-Physics and Astronomy"
    if (re.findall(r"-Psychology Emeriti", department)):
        department = "-Psychology"
    if (re.findall(r"-OPIE", department)):
        department = "-Ohio Program of Intensive English (OPIE)"
    if (re.findall(r"-Sociology & Anthropology", department)):
        department = "-Department of Sociology and Anthropology"
    if (re.findall(r"-Sociology & Anthropology Emeritus", department)):
        department = "-Department of Sociology and Anthropology"
    if (re.findall(r"-Women's, Gender, and Sexuality Studies", department)):
        department = "-Women's, Gender, and Sexuality Studies (WGSS)"

    try:
        address = soup.find("span", class_="cas_Office_Address").text
    except:
        pass

    email = soup.find("span", class_="cas_Email").text
    ohio_id = re.findall("(.*?)@ohio.edu", email)[0]

    try:
        phone = soup.find("span", class_="cas_Phone").text
    except:
        pass

    if (re.findall(r"\(?\d{3}\)?.+\d{3}.+\d{4}.+\(?\d{3}\)?.+\d{3}.+\d{4}", phone)):
        phone1 = re.findall(r"(\(?\d{3}\)?.+\d{3}.+\d{4}).+\(?\d{3}\)?.+\d{3}.+\d{4}", phone)[0]
        phone2 = re.findall(r"\(?\d{3}\)?.+\d{3}.+\d{4}.+(\(?\d{3}\)?.+\d{3}.+\d{4})", phone)[0]
    else:
        phone1 = phone

    bio_found = False

    try:
        bio = soup.find("div", class_="fullProfileBio")
        bio_found = True
    except:
        pass

    if (bio_found == True):
        errors, warnings, print_friendly_errors, error_line_string = find_errors(bio)

        try:
            fix_all(bio, errors)
        except:
            pass

        line = ""

        for tag in bio:
            line += tag.encode("utf-8")

        bio = line
        bio = str(bio).strip()
        bio = bio.replace("\n", "")
        bio = bio.replace("'", "\\'")

    #profile_page_url = "https://webcmsstage.oit.ohio.edu/cas/group/1/content/create/group_node%3Astaff_profile"
    profile_page_url = "https://webcms.ohio.edu/cas/group/1/content/create/group_node%3Astaff_profile"

    print("display_name = " + display_name)
    print("first_name = " + first_name)
    print("last_name = " + last_name)
    print("title = " + title)
    print("department = " + department)
    print("email = " + email)
    print("ohio_id = " + ohio_id)
    print("bio = " + bio)

    try:
        print("phone1 = " + phone1)
    except:
        pass
    try:
        print("phone2 = " + phone2)
    except:
        pass

    driver.get(profile_page_url)
    ohio_login(driver)
    wait = WebDriverWait(driver, 10)

    # Selenium XPATHs
    display_name_xpath = '//*[@id="edit-title-0-value"]'
    first_name_xpath = '//*[@id="edit-field-first-name-0-value"]'
    last_name_xpath = '//*[@id="edit-field-last-name-0-value"]'
    image_xpath = '//*[@id="edit-field-image-0-upload"]'
    alt_text_xpath = '//*[contains(@id, "edit-field-image-0-alt")]'
    title_xpath = '//*[@id="edit-field-title-0-value"]'
    department_xpath = '//*[@id="edit-field-department"]'
    address_xpath = '//*[@id="edit-field-office-address-0-value"]'
    profile_type_xpath = '//*[@id="edit-field-profile-type"]'
    ohio_id_xpath = '//*[@id="edit-field-ohio-id-0-value"]'
    email_xpath = '//*[@id="edit-field-email-0-value"]'
    phone1_xpath = '//*[@id="edit-field-phone-0-value"]'
    phone2_xpath = '//*[@id="edit-field-phone-1-value"]'
    display_settings_xpath = '/html/body/div[2]/div/main/div[4]/div/form/div/div[2]/div/details[6]/summary'
    view_mode_xpath = '//*[@id="edit-ds-switch"]'
    columns_xpath = '//*[@id="edit-column-number"]'
    save_xpath = '//*[@id="edit-submit"]'
    bio_xpath = '/html/body/div[2]/div/main/div[4]/div/form/div/div[1]/div[16]/div/div[1]/div/div/div/div/iframe'
    bio_js = "document.getElementsByTagName('body')[0].innerHTML='" + bio + "';"

    try:
        phone1_js = "document.getElementById('edit-field-phone-0-value').value = '" + phone1 + "';"
    except:
        pass
    try:
        phone2_js = "document.getElementById('edit-field-phone-1-value').value = '" + phone2 + "';"
    except:
        pass

    driver.find_element_by_xpath(display_settings_xpath).click()
    Select(driver.find_element_by_xpath(view_mode_xpath)).select_by_visible_text("Full Profile")
    Select(driver.find_element_by_xpath(columns_xpath)).select_by_visible_text("1")

    driver.find_element_by_xpath(display_name_xpath).send_keys(display_name)
    driver.find_element_by_xpath(first_name_xpath).send_keys(first_name)
    driver.find_element_by_xpath(last_name_xpath).send_keys(last_name)

    try:
        driver.find_element_by_xpath(title_xpath).send_keys(title)
    except:
        pass

    try:
        Select(driver.find_element_by_xpath(department_xpath)).select_by_visible_text(department)
    except:
        pass

    # Change this value for whatever web queue you are running
    profile = "Staff"
    Select(driver.find_element_by_xpath(profile_type_xpath)).select_by_visible_text(profile)

    try:
        driver.find_element_by_xpath(address_xpath).send_keys(address)
    except:
        pass

    driver.find_element_by_xpath(ohio_id_xpath).send_keys(ohio_id)
    driver.find_element_by_xpath(email_xpath).send_keys(email)

    try:
        driver.find_element_by_xpath(phone1_xpath).send_keys(phone1)
    except:
        pass

    try:
        driver.find_element_by_xpath(phone2_xpath).send_keys(phone2)
    except:
        pass

    driver.switch_to.frame(driver.find_element_by_xpath(bio_xpath))
    driver.execute_script(bio_js)

    try:
        driver.switch_to.default_content()
    except:
        pass

    try:
        file_name, image_title, alt_text = download_image(url, soup.find("div", class_="fullProfileImg"))
        driver.find_element_by_xpath(image_xpath).send_keys(os.getcwd() + "/images/" + file_name)
        wait.until(EC.presence_of_element_located((By.XPATH, alt_text_xpath)))
        alt_js = "document.querySelector(\"[id^='edit-field-image-0-alt']\").value=\"" + alt_text + "\";"
        driver.execute_script(alt_js)
    except:
        pass

    driver.find_element_by_xpath(save_xpath).click()

    # Accept alert
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

