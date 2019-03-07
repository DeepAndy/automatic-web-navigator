'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    This script migrates profile pages from the Chillothe branch
                campus to Ohio University Drupal pages.
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

'''
def convert_department(department):
    if (re.findall(r"Recreation [and]?|&? Sports? Pedagogy", department)):
        department = "Recreation and Sports Pedagogy"
    if (re.findall(r"Patton College Dean's Office", department)):
        department = "Dean's Office"
    if (re.findall(r"Counseling [and|&] Higher Education", department)):
        department = "Counseling and Higher Education"

    return department
'''

def script_main(driver, url, pos):
    page_source = driver.page_source
    page_source = page_source.replace(u"\xa0", u" ")
    page_source = page_source.replace(u"\xc2", u" ")
    soup = BeautifulSoup(page_source, features="html.parser")

    display_name = soup.find("div", class_="profile-full-name").text
    full_name = display_name.split()
    first_name = first_name = full_name[0]
    last_name = full_name[len(full_name) - 1]
    departments = []

    try:
        title = soup.find("span", class_="profile-title").text
        title = re.sub(r"(,)$", "", title)
    except:
        pass

    try:
        department = soup.find("span", class_="profile-department").text

        f = open("departments.txt", "r")
        f1 = open("departments.txt", "a+")

        departments = f.readlines()
        found_department = False

        for dep in departments:
            if (dep.strip() == department.strip()):
                found_department = True

        if (found_department == False):
            f1.write(department + "\n")
    except:
        pass

    degree_found = False

    try:
        degree = soup.find("div", class_="profile-degree-university").text
        degree_found = True
    except:
        pass

    if (degree_found == True and not re.findall(r"^\s*$", degree)):
        degree = "<p>" + degree + "</p>"
    
    try:
        address = soup.find("div", class_="profile-office-address").text
    except:
        pass

    try:
        tmp_soup = soup.find("div", class_="profile-email")
        email = tmp_soup.find("a").text
    except:
        ohio_id = first_name.lower() + last_name.lower()


    try:
        ohio_id = re.findall("(.*?)@ohiou?.edu", email)[0]
    except:
        ohio_id = first_name.lower() + last_name.lower()

    try:
        phone = soup.find("div", class_="profile-phone").text

        if (re.findall(r"\(?\d{3}\)?.+\d{3}.+\d{4}.+\(?\d{3}\)?.+\d{3}.+\d{4}", phone)):
            phone1 = re.findall(r"(\(?\d{3}\)?.+\d{3}.+\d{4}).+\(?\d{3}\)?.+\d{3}.+\d{4}", phone)[0]
            phone2 = re.findall(r"\(?\d{3}\)?.+\d{3}.+\d{4}.+(\(?\d{3}\)?.+\d{3}.+\d{4})", phone)[0]
        else:
            phone1 = phone
    except:
        pass

    bio_found = False

    try:
        bio = soup.find("div", class_="profile-bio-info")
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

        if (degree_found == True):
            bio = degree + bio
        
        if (re.findall(r"^\s*$", bio)):
            bio_found = False

        print("bio_found = " + str(bio_found))

    profile_page_url = "https://webcmsdev.oit.ohio.edu/group/436/content/create/group_node%3Astaff_profile"
    #profile_page_url = "https://webcms.ohio.edu/group/436/content/create/group_node%3Astaff_profile"

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
    link_to_full_xpath = '//*[@id="edit-field-link-to-full-profile-value"]'
    create_content_xpath = '//*[@id="edit-submit"]'

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
    bio_xpath = '//*[@id="cke_1_contents"]/iframe'
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
        file_name, image_title, alt_text = download_image(url, soup.find("div", class_="profile-img"))
        driver.find_element_by_xpath(image_xpath).send_keys(os.getcwd() + "/images/" + file_name)
        wait.until(EC.presence_of_element_located((By.XPATH, alt_text_xpath)))

        if (alt_text == "No alternative text available"):
            alt_text = display_name

        alt_js = "document.querySelector(\"[id^='edit-field-image-0-alt']\").value=\"" + alt_text + "\";"
        driver.execute_script(alt_js)
    except:
        pass

    if (bio_found == True):
        driver.find_element_by_xpath(link_to_full_xpath).click()

    driver.find_element_by_xpath(save_xpath).click()

    # Accept alert
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

    try:
        wait.until(EC.presence_of_element_located((By.XPATH, create_content_xpath)))
        driver.find_element_by_xpath(create_content_xpath).click()
    except:
        pass
