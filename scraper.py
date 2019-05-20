'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    This script aims to scrape pages for their content and replace
                within Drupal
Python 3.7.2
'''

import re
import time
import urllib
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ohio_login import ohio_login
from fix_html import *
from download_image_document import download_images_from_soup_return
from download_image_document import download_documents_from_soup
from date_converter import date_converter

'''
Function: scrape_article
Description: Scrapes article contents and moves them to Drupal
Parameters: driver (selenium webdriver), soup (BeautifulSoup object),
            content (BeautifulSoup object), config_value (regex)
'''
def scrape_article(driver, soup, content, config_value):
    wait = WebDriverWait(driver, 30)
    title = driver.title
    date_element_found = False
    scrape_date_id_found = False
    date_class_found = False

    # Read for article values of interest from config file
    f = open('scrape_values.txt', 'r')

    for value in f.readlines():
        if (re.search(r'date_element', value)):
            if (re.search(config_value, value)):
                date_element_found = True
                date_element = re.search(config_value, value).group(1)
        elif (re.search(r'date_id', value)):
            if (re.search(config_value, value)):
                scrape_date_id_found = True
                scrape_date_id = re.search(config_value, value).group(1)
        elif (re.search(r'date_class', value)):
            if (re.search(config_value, value)):
                date_class_found = True
                date_class = re.search(config_value, value).group(1)
        elif (re.search(r'webcms_node', value)):
            if (re.search(config_value, value)):
                webcms_node_found = True
                webcms_node = re.search(config_value, value).group(1)

    f.close()
    date_attributes = {}

    # Get date attributes
    if (scrape_date_id_found == True):
        date_attributes['id'] = scrape_date_id
    if (date_class_found == True):
        date_attributes['class'] = date_class

    # Get the date and convert to YYYY-MM-DD
    date = soup.find(date_element, attrs=date_attributes).text
    date = date_converter(date)

    # Get xpaths from drupal_article_ids
    f1 = open('drupal_article_ids.txt', 'r')

    # Read Drupal ids
    for value in f1.readlines():
        if (re.search(r'title_id', value)):
            if (re.search(config_value, value)):
                title_id = re.search(config_value, value).group(1)
        elif (re.search(r'date_id', value)):
            if (re.search(config_value, value)):
                drupal_date_id = re.search(config_value, value).group(1)
        elif (re.search(r'image_id', value)):
            if (re.search(config_value, value)):
                image_id = re.search(config_value, value).group(1)
        elif (re.search(r'image_alt_id_partial', value)):
            if (re.search(config_value, value)):
                image_alt_id_partial = re.search(config_value, value).group(1)
                image_alt_xpath = '//*[contains(@id, "' + image_alt_id_partial + '")]'
        elif (re.search(r'page_location_class', value)):
            if (re.search(config_value, value)):
                page_location_class = re.search(config_value, value).group(1)
        elif (re.search(r'parent_page_id', value)):
            if (re.search(config_value, value)):
                parent_page_id = re.search(config_value, value).group(1)
        elif (re.search(r'parent_page_option_text', value)):
            if (re.search(config_value, value)):
                parent_page_option_text = re.search(config_value, value).group(1)
        elif (re.search(r'page_url_slug_id', value)):
            if (re.search(config_value, value)):
                page_url_slug_id = re.search(config_value, value).group(1)
        elif (re.search(r'display_settings_id', value)):
            if (re.search(config_value, value)):
                display_settings_id = re.search(config_value, value).group(1)
        elif (re.search(r'columns_id', value)):
            if (re.search(config_value, value)):
                columns_id = re.search(config_value, value).group(1)
        elif (re.search(r'columns_num', value)):
            if (re.search(config_value, value)):
                columns_num = re.search(config_value, value).group(1)
        elif (re.search(r'article_type_id', value)):
            if (re.search(config_value, value)):
                article_type_id = re.search(config_value, value).group(1)
        elif (re.search(r'article_type_option_text', value)):
            if (re.search(config_value, value)):
                article_type_option_text = re.search(config_value, value).group(1)
        elif (re.search(r'save_id', value)):
            if (re.search(config_value, value)):
                save_id = re.search(config_value, value).group(1)

    # Connect to WebCMS create new article page
    driver.get(webcms_node)
    ohio_login(driver)

    # Add title
    wait.until(EC.visibility_of_element_located((By.ID, title_id)))
    driver.execute_script('document.getElementById("' + title_id + '").value="' + title + '";')

    # Add date
    wait.until(EC.visibility_of_element_located((By.ID, drupal_date_id)))
    driver.execute_script('document.getElementById("' + drupal_date_id + '").value="' + date + '";')

    # Download documents and images
    download_documents_from_soup(content)
    images = download_images_from_soup_return(content)

    # Upload images
    if (len(images) > 0):
        file_name = re.search(r'\..*/(.*\..*)', images[0]['src']).group(1)

        if (images[0].has_attr('alt')):
            if (re.search(r'^\s*$', images[0]['alt'])):
                alt_text = 'No alternative text available'
            else:
                alt_text = images[0]['alt']
        else:
            alt_text = 'No alternative text available'

        wait.until(EC.element_to_be_clickable((By.ID, image_id)))
        driver.find_element_by_id(image_id).send_keys(os.getcwd() + '/images/' + file_name)
        wait.until(EC.visibility_of_element_located((By.XPATH, image_alt_xpath)))
        driver.execute_script('document.querySelector("[id^=\'' + image_alt_id_partial + '\']").value="' + alt_text + '";')

    # Click page location
    driver.execute_script('document.getElementsByClassName("' + page_location_class + '")[0].click();')

    # Enter the value of the parent page
    wait.until(EC.visibility_of_element_located((By.ID, parent_page_id)))
    select = Select(driver.find_element_by_id(parent_page_id))
    select.select_by_visible_text(parent_page_option_text)

    # Enter the title into the page url slug
    wait.until(EC.visibility_of_element_located((By.ID, page_url_slug_id)))
    driver.execute_script('document.getElementById("' + page_url_slug_id + '").value="' + title + '";')

    # Click display settings
    wait.until(EC.visibility_of_element_located((By.ID, display_settings_id)))
    driver.find_element_by_id(display_settings_id).click()

    # Change number of columns
    wait.until(EC.visibility_of_element_located((By.ID, columns_id)))
    select = Select(driver.find_element_by_id(columns_id))
    select.select_by_visible_text(columns_num)

    # Change article type
    wait.until(EC.visibility_of_element_located((By.ID, article_type_id)))
    select = Select(driver.find_element_by_id(article_type_id))
    select.select_by_visible_text(article_type_option_text)

    # Fix HTML
    errors, warnings, print_friendly_errors, error_line_string = find_errors(content)
    fix_all(content, errors)

    output = ''

    for index in range(len(content.contents)):
        if (re.search('^\s*$', str(content.contents[index]))):
            pass
        else:
            output += str(content.contents[index])

    output = output.replace('"', '\\"')
    output = output.replace('\n', '')

    try:
        driver.execute_script('window.frames[1].document.getElementsByTagName("body")[0].innerHTML="' + output + '";')
    except Exception as e:
        print(e)

    # Press the save button
    wait.until(EC.element_to_be_clickable((By.ID, save_id)))
    driver.find_element_by_id(save_id).click()

    # Accept leave page alert
    try:
        driver.switch_to.alert.accept()
    except:
        pass

def script_main(driver, url, pos):
    # Set up page source and BeautifulSoup object
    page_source = driver.page_source
    page_source = page_source.replace(u'\xa0', u' ')
    page_source = page_source.replace(u'\xc2', u' ')
    page_source = page_source.replace('\n', ' ')
    soup = BeautifulSoup(page_source, features='html.parser')

    f = open('scrape_values.txt', 'r')

    content_element_found = False
    content_id_found = False
    content_class_found = False
    content_xpath_found = False
    scrape_type_found = False

    config_value = re.compile('=\s*(.+)')

    # Evaluate our config file
    for value in f.readlines():
        if (re.search(r'content_element', value)):
            if (re.search(config_value, value)):
                content_element_found = True
                content_element = re.search(config_value, value).group(1)
        elif (re.search(r'content_id', value)):
            if (re.search(config_value, value)):
                content_id_found = True
                content_id = re.search(config_value, value).group(1)
        elif (re.search(r'content_class', value)):
            if (re.search(config_value, value)):
                content_class_found = True
                content_class = re.search(config_value, value).group(1)
        elif (re.search(r'scrape_type', value)):
            if (re.search(config_value, value)):
                scrape_type_found = True
                scrape_type = re.search(config_value, value).group(1)

    f.close()

    if (scrape_type_found == False):
        print('You must provide a scrape type')
        return

    content_attributes = {}

    # Set up attributes
    if (content_id_found == True):
        content_attributes['id'] = content_id
    if (content_class_found == True):
        content_attributes['class'] = content_class

    if (content_element_found == True and len(content_attributes) > 0):
        content = soup.find(content_element, attrs=content_attributes)
    elif (content_element_found == False and len(content_attributes) > 0):
        content = soup.find(attrs=content_attributes)
    else:
        return

    if (scrape_type == 'article'):
        scrape_article(driver, soup, content, config_value)
