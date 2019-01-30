import urllib                                                                    
import re
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

'''
Author:         Austin Moore
Script Type:    Helper Script
Description:    Download and upload images to Drupal
'''

'''
Function:       download_image()
Arguments:      string, soup object
Description:    Download first image from a web page without Selenium.
Notes:          This function will assume you only want the first image from
                the soup content you pass it. Therefore, you must remove
                images in the DOM if you are calling this function in a loop.
'''

def download_image(url, content):
    content = str(content)
    soup = BeautifulSoup(content, features="html.parser")
    images = soup.find_all("img")
    main_url = re.findall(r"\//(.+?)/", url)[0]
    index = 0

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

    if (alt_text == ""):
        alt_text = "No alternative text available"

    if (image_source.find("/") == 0):
        image_source = "https://" + main_url + image_source

    try:
        urllib.urlretrieve(image_source, "images/" + file_name)
    except:
        print("Failed to download image at \"" + image_source + "\"")

    return file_name, image_title, alt_text

def embed_image(driver,file_name, image_title, alt_text):
    wait = WebDriverWait(driver, 10)

    image_embed_xpath = '//*[@id="cke_38"]/span[1]'
    iframe_xpath = '//*[@id="entity_browser_iframe_media_embed2"]'
    add_new_image_xpath = '//*[@id="entity-browser-media-embed2-form"]/nav/ul/li[2]/a'
    image_upload_xpath = '//*[@id="edit-inline-entity-form-field-media-image-0-upload"]'
    name_xpath = '//*[@id="edit-inline-entity-form-name-0-value"]'
    alternative_text_xpath = '//*[contains(@id, "edit-inline-entity-form-field-media-image-0-alt")]'
    save_image_xpath = '//*[@id="edit-submit"]'
    embed_xpath = '/html/body/div[6]/div[3]/div/button[2]'

    driver.find_element_by_xpath(image_embed_xpath).click()

    wait.until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
    element = driver.find_element_by_xpath(iframe_xpath)
    driver.switch_to.frame(element)

    driver.find_element_by_xpath(add_new_image_xpath).click()

    element = driver.find_element_by_xpath(image_upload_xpath)
    element.send_keys(os.getcwd() + "/images/" + file_name)

    driver.find_element_by_xpath(name_xpath).send_keys(image_title)

    wait.until(EC.presence_of_element_located((By.XPATH, alternative_text_xpath)))
    driver.find_element_by_xpath(alternative_text_xpath).send_keys(alt_text)

    driver.find_element_by_xpath(save_image_xpath).click()

    wait.until(EC.presence_of_element_located((By.XPATH, embed_xpath)))
    driver.find_element_by_xpath(embed_xpath).click()
