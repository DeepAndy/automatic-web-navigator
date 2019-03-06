'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    This script migrates profile pages from the Patton College of
                Education to Ohio University Drupal pages
Python 3.7.2
'''

import re
import time
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

def convert_department(department):
    if (re.findall(r"Recreation [and]?|&? Sports? Pedagogy", department)):
        department = "Recreation and Sports Pedagogy"
    if (re.findall(r"Patton College Dean's Office", department)):
        department = "Dean's Office"
    if (re.findall(r"Counseling [and|&] Higher Education", department)):
        department = "Counseling and Higher Education"

    return department

def script_main(driver, url, pos):
    page_source = driver.page_source
    page_source = page_source.replace(u"\xa0", u" ")
    page_source = page_source.replace(u"\xc2", u" ")
    soup = BeautifulSoup(page_source, features="html.parser")

    try:
        display_name = soup.find("h1", class_="fullProfileName").text
    except:
        print
        print("Can not find any content")
        return

    full_name = display_name.split()
    first_name = full_name[0]
    last_name = full_name[len(full_name) - 1]
    split = False
    found_department_field = False
    title = ""
    department = ""
    f = open("departments.txt", "a+")
    f1 = open("departments.txt", "r")
    department_list = f1.readlines()
    found_department_list = False

    try:
        department = soup.find("span", class_="edu_Department").text
        department = convert_department(department)

        if (re.findall(r"^\s*$", department)):
            found_department_field = False
        else:
            found_department_field = True
    except:
        pass

    print("found department = " + str(found_department_field))

    if (re.findall(r"^.*?, ?.*?$", soup.find("span", class_="edu_Title").text)):
        title_split = re.split(r", ?", soup.find("span", class_="edu_Title").text)
        split = True
    else:
        title = soup.find("span", class_="edu_Title").text

    if (found_department_field == True and split == True):
        if (title_split[1] == department):
            title = title_split[0]
        else:
            title = soup.find("span", class_="edu_Title").text

    print("split = " + str(split))

    if (found_department_field == False and split == True):
        title = title_split[0]
        department = title_split[1]
        department = convert_department(department)

    print(department_list)

    for dep in department_list:
        if (dep.strip() == department.strip()):
            found_department_list = True

    if (found_department_list == False):
        print("Department not in list")
        f.write(department + "\n")
    else:
        print("Department in list")

    '''
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
    '''

    try:
        address = soup.find("span", class_="edu_Office_Address").text
    except:
        pass

    try:
        email = soup.find("span", class_="edu_Email").text
    except:
        ohio_id = first_name.lower() + last_name.lower()

    try:
        ohio_id = re.findall("(.*?)@ohiou?.edu", email)[0]
    except:
        ohio_id = first_name.lower() + last_name.lower()

    try:
        phone = soup.find("span", class_="edu_Phone").text
    except:
        pass

    if (re.findall(r"\(?\d{3}\)?.+\d{3}.+\d{4}.+\(?\d{3}\)?.+\d{3}.+\d{4}", phone)):
        phone1 = re.findall(r"(\(?\d{3}\)?.+\d{3}.+\d{4}).+\(?\d{3}\)?.+\d{3}.+\d{4}", phone)[0]
        phone2 = re.findall(r"\(?\d{3}\)?.+\d{3}.+\d{4}.+(\(?\d{3}\)?.+\d{3}.+\d{4})", phone)[0]
    else:
        phone1 = phone

    bio_found = False

    try:
        bio = soup.find("div", class_="profileBio")
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
            line += str(tag)

        bio = line
        bio = str(bio).strip()
        bio = bio.replace("\n", "")
        bio = bio.replace("'", "\\'")

    #profile_page_url = "https://webcmsdev.oit.ohio.edu/education/group/1/content/create/group_node%3Astaff_profile"
    profile_page_url = "https://webcms.ohio.edu/education/group/1/content/create/group_node%3Astaff_profile"

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
    display_name = display_name.replace("'", "\\'")
    first_name = first_name.replace("'", "\\'")
    last_name = last_name.replace("'", "\\'")
    display_name_js = "document.getElementById('edit-title-0-value').value = '" + display_name + "';"
    first_name_js = "document.getElementById('edit-field-first-name-0-value').value = '" + first_name + "';"
    last_name_js = "document.getElementById('edit-field-last-name-0-value').value = '" + last_name + "';"
    image_xpath = '//*[@id="edit-field-image-0-upload"]'
    alt_text_xpath = '//*[contains(@id, "edit-field-image-0-alt")]'
    try:
        title_js = "document.getElementById('edit-field-title-0-value').value = '" + title + "';"
    except:
        pass
    department_xpath = '//*[@id="edit-field-education-tags"]'
    try:
        address_js = "document.getElementById('edit-field-office-address-0-value').value = '" + address + "';"
    except:
        pass
    address_xpath = '//*[@id="edit-field-office-address-0-value"]'
    ohio_id_js = "document.getElementById('edit-field-ohio-id-0-value').value = '" + ohio_id + "';"
    email_js = "document.getElementById('edit-field-email-0-value').value = '" + email + "';"
    try:
        phone1_js = "document.getElementById('edit-field-phone-0-value').value = '" + phone1 + "';"
    except:
        pass
    try:
        phone2_js = "document.getElementById('edit-field-phone-1-value').value = '" + phone2 + "';"
    except:
        pass
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

    driver.execute_script(display_name_js)
    driver.execute_script(first_name_js)
    driver.execute_script(last_name_js)

    try:
        driver.execute_script(title_js)
    except:
        pass

    try:
        Select(driver.find_element_by_xpath(department_xpath)).select_by_visible_text(department)
    except:
        pass

    try:
        driver.execute_script(address_js)
    except:
        pass

    driver.execute_script(ohio_id_js)
    driver.execute_script(email_js)

    try:
        driver.execute_script(phone1_js)
    except:
        pass

    try:
        driver.execute_script(phone2_js)
    except:
        pass

    driver.switch_to.frame(driver.find_element_by_xpath(bio_xpath))
    driver.execute_script(bio_js)

    try:
        driver.switch_to.default_content()
    except:
        pass

    try:
        file_name, image_title, alt_text = download_image(url, soup.find("div", class_="profileImg"))
        driver.find_element_by_xpath(image_xpath).send_keys(os.getcwd() + "/images/" + file_name)
        wait.until(EC.presence_of_element_located((By.XPATH, alt_text_xpath)))

        if (alt_text == "No alternative text available"):
            alt_text = display_name

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

