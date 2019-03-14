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
    element = Select(driver.find_element_by_xpath(parent_page_xpath))
    #element.select_by_visible_text(parent_page)
    element.select_by_index(1)

    # Slug
    driver.execute_script("document.getElementById('edit-slug').value='" + title + "';")

    # Clean and paste HTML
    wait.until(EC.element_to_be_clickable((By.XPATH, source_xpath)))
    driver.find_element_by_xpath(source_xpath).click()
    source_on = True
    content = driver.find_element_by_xpath(textarea_xpath).get_attribute("value")
    content = BeautifulSoup(content, "html.parser")

    errors, warnings, print_friendly_errors, error_line_string = find_errors(content)

    try:
        content = fix_all(content, errors)
    except:
        print("Skipped HTML cleanup")

    first = True

    for tag in content.find_all():
        print(str(tag))
        if (tag.name == "img"):
            if (source_on == True):
                wait.until(EC.element_to_be_clickable((By.XPATH, source_xpath)))
                driver.find_element_by_xpath(source_xpath).click()
                source_on = False

            try:
                file_name, image_title, alt_text = download_image(received_url, content)
                tag.decompose()
            except:
                print("Failed image download")
                continue

            try:
                driver.find_element_by_xpath(rich_text_xpath).click()
                embed_image(driver, file_name, image_title, alt_text)
            except:
                print("Failed image embed")
                continue
        else:
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

            if (not re.findall("\S+", line)):
                continue

            if (first == False):
                html_backup = driver.find_element_by_xpath(textarea_xpath).get_attribute("value")
                full = html_backup + line
            else:
                full = line
                first = False

            full = full.strip()
            full = full.replace("\n", "")
            full = full.replace('"', '\\"')

            if (re.findall("\S+", full)):
                body_textarea_script = 'document.getElementById("cke_1_contents").getElementsByClassName("cke_source")[0].value="' + full + '";'
                driver.execute_script(body_textarea_script)

    driver.switch_to.default_content()
    time.sleep(30)

    '''
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

    # Create content button
    element = driver.find_element_by_xpath(create_content_xpath)
    element.click()
    '''
