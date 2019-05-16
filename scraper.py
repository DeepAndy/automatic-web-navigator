'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    This script aims to scrape pages for their content and replace
                within Drupal
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
from fix_html import *
from download_image_document import download_images_from_soup
from download_image_document import download_documents_from_soup
from date_converter import date_converter

'''
Function: scrape_article()
Description: Scrapes article contents and moves them to Drupal
Parameters: driver (selenium webdriver), soup (BeautifulSoup object),
            content (BeautifulSoup object), config_value (regex)
'''
def scrape_article(driver, soup, content, config_value):
    title = driver.title
    date_element_found = False
    date_id_found = False
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
                date_id_found = True
                date_id = re.search(config_value, value).group(1)
        elif (re.search(r'date_class', value)):
            if (re.search(config_value, value)):
                date_class = True
                date_class = re.search(config_value, value).group(1)

    date_attributes = {}

    if (date_id_found == True):
        date_attributes['id'] = date_id
    if (date_class_found == True):
        date_attributes['class'] = date_class

    date = soup.find(date_element, attrs=date_attributes).text
    date = date_converter(date)

    download_documents_from_soup(content)

def script_main(driver, url, pos):
    # Set up page source and BeautifulSoup object
    page_source = driver.page_source
    page_source = page_source.replace(u"\xa0", u" ")
    page_source = page_source.replace(u"\xc2", u" ")
    soup = BeautifulSoup(page_source, features="html.parser")

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
        content = soup.find(content_element, attrs=content_attributes)
    else:
        return

    errors, warnings, print_friendly_errors, error_line_string = find_errors(content)
    fix_all(content, errors)

    if (scrape_type == 'article'):
        scrape_article(driver, soup, content, config_value)
