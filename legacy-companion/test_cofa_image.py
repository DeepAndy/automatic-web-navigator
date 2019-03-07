'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    Testing script for embedding images on COFA
Python 2.7.10
'''

import urllib
import re
import getpass
import time
import os
from ohio_login import ohio_login
from bs4 import BeautifulSoup

def script_main(driver, url, pos):                                               
    page_source = driver.page_source                                             
    page_source = page_source.replace(u"\xa0", u"")                              
    page_source = page_source.replace(u"\xc2", u"")                              
    soup = BeautifulSoup(page_source, features="html.parser")                    
    images = soup.find_all("img")                                                

    image_embed_xpath = '//*[@id="cke_38"]/span[1]'
    iframe_xpath = '//*[@id="entity_browser_iframe_media_embed2"]'
    add_new_image_xpath = '//*[@id="entity-browser-media-embed2-form"]/nav/ul/li[2]/a'
    image_upload_xpath = '//*[@id="edit-inline-entity-form-field-media-image-0-upload"]'
    name_xpath = '//*[@id="edit-inline-entity-form-name-0-value"]'
    alternative_text_xpath = '//*[contains(@id, "edit-inline-entity-form-field-media-image-0-alt")]'
    #//*[@id="edit-inline-entity-form-field-media-image-0-alt--tEgL067TBlQ"]
    save_image_xpath = '//*[@id="edit-submit"]'
    embed_xpath = '/html/body/div[6]/div[3]/div/button[2]'

    i = 1

    for image in images:                                                         
        try:                                                                     
            print(image)                                                         
            image_source = "https://ohio.edu" + image["src"] 
            print("image_source = " + image_source)                              
            urllib.urlretrieve(image_source, "images/" + str(i) + ".jpg")        
            i += 1                                                               
        except:                                                                  
            continue

    # FINE ARTS
    # basic_page_url = "https://webcmsdev.oit.ohio.edu/fine-arts/group/1/content/create/group_node%3Apage"
    # OIT
    basic_page_url = "https://webcmsdev.oit.ohio.edu/group/286/content/create/group_node%3Apage"

    driver.get(basic_page_url)

    ohio_login(driver)

    driver.get(basic_page_url)

    time.sleep(2)

    element = driver.find_element_by_xpath(image_embed_xpath)
    element.click()

    time.sleep(2)

    element = driver.find_element_by_xpath(iframe_xpath)
    driver.switch_to.frame(element)

    time.sleep(2)

    element = driver.find_element_by_xpath(add_new_image_xpath)
    element.click()

    time.sleep(2)

    element = driver.find_element_by_xpath(image_upload_xpath)
    element.send_keys(os.getcwd() + "/images/2.jpg")

    time.sleep(2)

    element = driver.find_element_by_xpath(name_xpath)
    element.send_keys("Testing")

    time.sleep(2)

    element = driver.find_element_by_xpath(alternative_text_xpath)
    element.send_keys("Testing")

    time.sleep(2)

    element = driver.find_element_by_xpath(save_image_xpath)
    element.click()

    time.sleep(2)

    element = driver.find_element_by_xpath(embed_xpath)
    element.click()

    time.sleep(20)
