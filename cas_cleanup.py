'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    This script migrates websites from Ohio University's
                Scripps College site into Drupal. Used in conjunction
                with navigator.py
Python 3.7.2
'''

import re
import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fix_html import *
from drupal_image import *
from ohio_login import ohio_login

def script_main(driver, received_url, pos):
    if (driver.current_url != received_url):
        ohio_login(driver)
        driver.get(received_url)

    wait = WebDriverWait(driver, 30)

    title_xpath = "//*[@id='edit-title-0-value']"
    page_location_xpath = '//*[@id="edit-page-location"]/summary'
    parent_page_xpath = '//*[@id="edit-parent-page"]'
    page_url_slug_xpath = '//*[@id="edit-slug"]'
    save_xpath = "//*[@id='edit-submit']"
    create_content_xpath = "//*[@id='edit-submit']"
    source_xpath = '//*[@id="cke_12"]'
    textarea_xpath = '/html/body/div[2]/div/main/div[5]/div/form/div/div[1]/div[6]/div/div[2]/div/div/div/div/textarea'
    rich_text_xpath = '//*[@id="cke_1_contents"]/iframe'
    rich_text_body_xpath = '/html/body'
    overlay_xpath = '//*[@class="ui-widget-overlay ui-front"]'
    first = True

    # Get title for the slug
    wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))
    title = driver.find_element_by_xpath(title_xpath).get_attribute("value")

    # Page location drop down
    wait.until(EC.element_to_be_clickable((By.XPATH, page_location_xpath)))
    driver.find_element_by_xpath(page_location_xpath).click()

    # Set parent page in select menu
    try:
        element = Select(driver.find_element_by_xpath(parent_page_xpath))
        element.select_by_index(1)
    except:
        pass

    # Slug
    try:
        driver.execute_script("document.getElementById('edit-slug').value='" + title + "';")
    except:
        pass

    # Clean and paste HTML
    wait.until(EC.element_to_be_clickable((By.XPATH, source_xpath)))
    driver.find_element_by_xpath(source_xpath).click()
    source_on = True
    content = driver.find_element_by_xpath(textarea_xpath).get_attribute("value")
    content = BeautifulSoup(content, "html.parser")

    errors, warnings, print_friendly_errors, error_line_string = find_errors(content)

    folder_title = title
    folder_title = folder_title.replace(" ", "-")
    folder_title = folder_title.replace("_", "-")
    folder_title = re.sub(r"[^A-Za-z0-9\-]", "", folder_title)

    if (not os.path.exists("cas_originals/" + folder_title + ".html")):
        original = open("cas_originals/" + folder_title + ".html", "w")
        original.write(str(content))

    all_documents = content.find_all("a", href=True)

    if (len(all_documents) > 0):
        images_folder, documents_folder = image_init()

        for document in all_documents:
            try:
                download_document_source(received_url, document, documents_folder)
            except:
                pass

    all_images = content.find_all()

    images_folder, documents_folder = image_init()
    images_folder += folder_title

    counter = 1

    if (content.find_all("img")):
        while (True):
            if (not os.path.exists(images_folder)):
                os.mkdir(images_folder)
                break
            else:
                counter += 1
                images_folder = re.sub(r"\d*$", "", images_folder)
                images_folder += str(counter)
                continue

        images_folder += "/"

        if (not os.path.exists(images_folder + "details.txt")):
            image_details = open(images_folder + "details.txt", "w")

            for tag in all_images:
                if (tag.name == "img"):
                    try:
                        file_name, folder_title, alt_text, link_text = download_image_source(received_url, all_images, images_folder)
                        image_details.write("File Name:          " + file_name + "\n")
                        image_details.write("Image Title:        " + folder_title + "\n")
                        image_details.write("Alternative Text:   " + alt_text + "\n")
                        image_details.write("Link:               " + link_text + "\n\n")
                        tag.decompose()
                    except:
                        pass

    try:
        content = fix_all(content, errors)
    except:
        print("Skipped HTML cleanup")

    added_tags = []

    for tag in content.find_all():
        if (tag.parent not in added_tags):
            if (source_on == False):
                wait.until(EC.invisibility_of_element_located((By.XPATH, overlay_xpath)))
                wait.until(EC.element_to_be_clickable((By.XPATH, source_xpath)))
                driver.find_element_by_xpath(source_xpath).click()
                source_on = True

            try:
                driver.switch_to.frame(driver.find_element_by_xpath(rich_text_xpath))
            except:
                pass

            line = str(tag)
            line = line.strip()
            line = line.replace("\n", "")
            line = line.replace('"', '\\"')

            if (not re.findall("\S+", line)):
                continue

            if (first == True):
                driver.execute_script('document.getElementById("cke_1_contents").getElementsByClassName("cke_source")[0].value="";')
                first = False

            body_textarea_script = 'document.getElementById("cke_1_contents").getElementsByClassName("cke_source")[0].value+="' + line + '";'
            driver.execute_script(body_textarea_script)

        added_tags.append(tag)

    driver.switch_to.default_content()

    # Click save button
    wait.until(EC.presence_of_element_located((By.XPATH, save_xpath)))
    element = driver.find_element_by_xpath(save_xpath)
    element.click()

    # Accept alert
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

    '''
    # Create content button
    element = driver.find_element_by_xpath(create_content_xpath)
    element.click()
    '''
