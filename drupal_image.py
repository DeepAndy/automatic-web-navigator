import urllib.request
import re
import os
import time
import configparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

'''
Author:         Austin Moore
Script Type:    Helper Script
Description:    Download and upload images to Drupal
Python 3.7.2 (Not working fully yet)
'''

'''
Function:       download_image()
Arguments:      string, soup object
Description:    Download first image from a web page without Selenium.
Notes:          This function will assume you only want the first image from
                the soup content you pass it. Therefore, you must remove
                images in the DOM if you are calling this function in a loop.
'''

def image_init():
    config = configparser.ConfigParser()
    config_file = "config_awn.ini"
    config.read(config_file)
    sections = config.sections()
    drupal_images_section = "drupal-images"
    drupal_documents_section = "drupal-documents"

    images_folder = config[drupal_images_section]["images_folder"]
    documents_folder = config[drupal_documents_section]["documents_folder"]

    return images_folder, documents_folder

def download_document_source(url, content, documents_folder):
    content = str(content)
    soup = BeautifulSoup(content, features="html.parser")
    documents = soup.find_all("a")

    anchor = documents[0]

    if (anchor.has_attr("href")):
        if (re.findall(r"\.pdf", anchor["href"])):
            document = anchor["href"]
        elif (re.findall(r"\.docx?", anchor["href"])):
            document = anchor["href"]
        elif (re.findall(r"\.pptx?", anchor["href"])):
            document = anchor["href"]
        elif (re.findall(r"\.xlsx?", anchor["href"])):
            document = anchor["href"]
        elif (re.findall(r'\.zip', anchor["href"])):
            document = anchor["href"]
        else:
            return

    file_name = re.findall(r"/([^/]+\.\w+)$", document)[0]

    if (document.find("/") == 0):
        document = "https://www.ohio.edu" + document

    try:
        urllib.request.urlretrieve(document, documents_folder + file_name)
    except:
        print("Failed to download document at: " + document)

def download_image_source(url, content, images_folder):
    content = str(content)
    soup = BeautifulSoup(content, features="html.parser")
    images = soup.find_all("img")
    main_url = re.findall(r"\//(.+?)/", url)[0]
    index = 0
    link_text = ""

    image = images[0]

    try:
        image_source = image["src"]
    except:
        return

    if (image.has_attr("alt")):
        alt_text = image["alt"]
    else:
        alt_text = "No alternative text available"

    file_name = re.findall(r"/([^/]+\.\w+)$", image_source)[0]
    image_title = re.findall(r"(.+?)\.", file_name)[0]

    if (not re.findall("\S+", alt_text)):
        alt_text = "No alternative text available"

    if (image_source.find("/") == 0):
        image_source = "https://www.ohio.edu" + image_source
    
    try:
        urllib.request.urlretrieve(image_source, images_folder + file_name)
    except:
        print("Failed to download image at \"" + image_source + "\"")

    if (image.parent.name == "a" and image.parent.has_attr("href")):
        link_text = image.parent["href"]

    if (link_text.find("/") == 0):
        link_text = "https://www.ohio.edu" + link_text

    return file_name, image_title, alt_text, link_text


def download_image(url, content):
    content = str(content)
    soup = BeautifulSoup(content, features="html.parser")
    images = soup.find_all("img")
    main_url = re.findall(r"\//(.+?)/", url)[0]
    index = 0
    link_text = ""

    image = images[0]

    try:
        image_source = image["src"]
    except:
        return

    if (image.has_attr("alt")):
        alt_text = image["alt"]
    else:
        alt_text = "No alternative text available"

    file_name = re.findall(r"/([^/]+\.\w+)$", image_source)[0]
    image_title = re.findall(r"(.+?)\.", file_name)[0]

    if (not re.findall("\S+", alt_text)):
        alt_text = "No alternative text available"

    if (image_source.find("/") == 0):
        image_source = "https://www.ohio.edu" + image_source
    
    try:
        urllib.request.urlretrieve(image_source, "images/" + file_name)
    except:
        print("Failed to download image at \"" + image_source + "\"")

        return

    if (image.has_attr("alt")):
        alt_text = image["alt"]
    else:
        alt_text = "No alternative text available"

    file_name = re.findall(r"/([^/]+\.\w+)$", image_source)[0]
    image_title = re.findall(r"(.+?)\.", file_name)[0]

    if (not re.findall("\S+", alt_text)):
        alt_text = "No alternative text available"

    if (image_source.find("/") == 0):
        image_source = "https://www.ohio.edu" + image_source
    
    try:
        urllib.request.urlretrieve(image_source, "images/" + file_name)
    except:
        print("Failed to download image at \"" + image_source + "\"")

    if (image.parent.name == "a" and image.parent.has_attr("href")):
        link_text = image.parent["href"]

    if (link_text.find("/") == 0):
        link_text = "https://www.ohio.edu" + link_text

    return file_name, image_title, alt_text, link_text

def embed_image(driver,file_name, image_title, alt_text, link_text):
    wait = WebDriverWait(driver, 30)

    image_embed_xpath = '//*[@id="cke_37"]'
    iframe_xpath = '//*[@id="entity_browser_iframe_media_embed2"]'
    add_new_image_xpath = '//*[@id="entity-browser-media-embed2-form"]/nav/ul/li[2]/a'
    image_upload_xpath = '//*[@id="edit-inline-entity-form-field-media-image-0-upload"]'
    name_xpath = '//*[@id="edit-inline-entity-form-name-0-value"]'
    alternative_text_xpath = '//*[contains(@id, "edit-inline-entity-form-field-media-image-0-alt")]'
    save_image_xpath = '//*[@id="edit-submit"]'
    link_xpath = '//*[contains(@id, "edit-attributes-data-entity-embed-display-settings-link-url")]'
    embed_xpath = '/html/body/div[6]/div[3]/div/button[2]'

    driver.find_element_by_xpath(image_embed_xpath).click()

    wait.until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
    element = driver.find_element_by_xpath(iframe_xpath)
    driver.switch_to.frame(element)

    driver.find_element_by_xpath(add_new_image_xpath).click()
