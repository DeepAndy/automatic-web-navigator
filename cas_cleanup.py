'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    This script migrates websites from Ohio University's
                Scripps College site into Drupal. Used in conjunction
                with navigator.py
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
from ohio_login import ohio_login

def script_main(driver, received_url, pos):
    if (driver.current_url != received_url):
        ohio_login(driver)
        driver.get(received_url)

    wait = WebDriverWait(driver, 10)

    title_xpath = "//*[@id='edit-title-0-value']"
    page_location_xpath = '//*[@id="edit-page-location"]/summary'
    parent_page_xpath = '//*[@id="edit-parent-page"]'
    page_url_slug_xpath = '//*[@id="edit-slug"]'
    save_xpath = "//*[@id='edit-submit']"
    create_content_xpath = "//*[@id='edit-submit']"
    rich_text_xpath = '//*[@id="cke_1_contents"]/iframe'
    rich_text_body_xpath = '/html/body'
    first = True

    if (received_url.find("/cas/group/6/nodes")):
        parent_page = "/cas/sociology-anthropology"
    elif (received_url.find("/cas/group/11/nodes")):
        parent_page = "/cas/political-science"
    elif (received_url.find("/cas/group/16/nodes")):
        parent_page = "/cas/geology"
    elif (received_url.find("/cas/group/21/nodes")):
        parent_page = "/cas/history"
    elif (received_url.find("/cas/group/26/nodes")):
        parent_page = "/cas/nqpi"
    elif (received_url.find("/cas/group/31/nodes")):
        parent_page = "/cas/linguistics"
    elif (received_url.find("/cas/group/36/nodes")):
        parent_page = "/cas/about"
    elif (received_url.find("/cas/group/41/nodes")):
        parent_page = "/cas/dean"
    elif (received_url.find("/cas/group/46/nodes")):
        parent_page = "/cas/contemporary-history"
    elif (received_url.find("/cas/group/51/nodes")):
        parent_page = "/cas/law-center"
    elif (received_url.find("/cas/group/56/nodes")):
        parent_page = "/cas/plant-biology"
    elif (received_url.find("/cas/group/61/nodes")):
        parent_page = "/cas/psychology"
    elif (received_url.find("/cas/group/66/nodes")):
        parent_page = "/cas/english"
    elif (received_url.find("/cas/group/71/nodes")):
        parent_page = "/cas/chemistry"
    elif (received_url.find("/cas/group/76/nodes")):
        parent_page = "/cas/wgss"
    elif (received_url.find("/cas/group/81/nodes")):
        parent_page = "/cas/graduate"
    elif (received_url.find("/cas/group/86/nodes")):
        parent_page = "/cas/biology"
    elif (received_url.find("/cas/group/91/nodes")):
        parent_page = "/cas/physics-astronomy"
    elif (received_url.find("/cas/group/96/nodes")):
        parent_page = "/cas/african-american-studies"
    elif (received_url.find("/cas/group/101/nodes")):
        parent_page = "/cas/undergraduate"
    elif (received_url.find("/cas/group/106/nodes")):
        parent_page = "/cas/philosophy"
    elif (received_url.find("/cas/group/111/nodes")):
        parent_page = "/cas/classics"
    elif (received_url.find("/cas/group/116/nodes")):
        parent_page = "/cas/economics"
    elif (received_url.find("/cas/group/121/nodes")):
        parent_page = "/cas/math"
    elif (received_url.find("/cas/group/126/nodes")):
        parent_page = "/cas/genomics"
    elif (received_url.find("/cas/group/131/nodes")):
        parent_page = "/cas/alumni"
    elif (received_url.find("/cas/group/136/nodes")):
        parent_page = "/cas/contact"
    elif (received_url.find("/cas/group/141/nodes")):
        parent_page = "/cas/phi-beta-kappa"
    elif (received_url.find("/cas/group/146/nodes")):
        parent_page = "/cas/molecular-cellular-biology"
    elif (received_url.find("/cas/group/151/nodes")):
        parent_page = "/cas/ocees"
    elif (received_url.find("/cas/group/156/nodes")):
        parent_page = "/cas/quantitative-biology"
    elif (received_url.find("/cas/group/161/nodes")):
        parent_page = "/cas/ping-institute"
    elif (received_url.find("/cas/group/166/nodes")):
        parent_page = "/cas/modern-languages"
    elif (received_url.find("/cas/group/171/nodes")):
        parent_page = "/cas/opie"
    elif (received_url.find("/cas/group/176/nodes")):
        parent_page = "/cas/geography"

    # Get title for the slug
    wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))
    title = driver.find_element_by_xpath(title_xpath).get_attribute("value")

    # Page location drop down
    wait.until(EC.presence_of_element_located((By.XPATH, page_location_xpath)))
    driver.find_element_by_xpath(page_location_xpath).click()

    '''
    # Set parent page in select menu
    element = Select(driver.find_element_by_xpath(parent_page_xpath))
    element.select_by_visible_text(parent_page)
    '''

    # Slug
    driver.find_element_by_xpath(page_url_slug_xpath).send_keys(title)

    # Clean and paste HTML
    driver.switch_to.frame(driver.find_element_by_xpath(rich_text_xpath))
    content = driver.find_element_by_xpath(rich_text_body_xpath).get_attribute("innerHTML")
    content = BeautifulSoup(content, "html.parser")

    errors, warnings, print_friendly_errors, error_line_string = find_errors(content)

    try:
        fix_all(content, errors)
    except:
        print("Skipped HTML cleanup")

    content = str(content)
    content = content.replace('"', '\\"')
    content = content.strip()
    content = content.replace("\n", "")

    body_textarea_script = 'document.getElementsByTagName("body")[0].innerHTML="' + str(content) + '";'
    driver.execute_script(body_textarea_script)
    driver.switch_to.default_content()
    time.sleep(10)

    # Click save button
    wait.until(EC.presence_of_element_located((By.XPATH, save_xpath)))
    element = driver.find_element_by_xpath(save_xpath)
    element.click()

    '''
    # Accept alert
    alert = driver.switch_to.alert
    alert.accept()
    '''

    '''
    # Create content button
    element = driver.find_element_by_xpath(create_content_xpath)
    element.click()
    '''
