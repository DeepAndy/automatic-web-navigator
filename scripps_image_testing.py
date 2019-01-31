'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    This script migrates websites from Ohio University's
                Scripps College site into Drupal. Used in conjunction
                with navigator.py
'''

import re
import time
import io
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fix_html import *
from ohio_login import ohio_login
from drupal_image import *

def script_main(driver, received_url, pos):
    page_source = driver.page_source
    page_source = page_source.replace(u"\xa0", u" ")
    page_source = page_source.replace(u"\xc2", u" ")
    soup = BeautifulSoup(page_source, "html.parser")
    article_page_url = "https://webcmsdev.oit.ohio.edu/group/461/content/create/group_node%3Aarticle"

    title = ""
    author = ""
    story_date = ""
    date = ""

    title = driver.title

    '''
    f = io.open("title.txt", "r", encoding="utf-8")
    all_sites = f.readlines()

    for site in all_sites:
        site = site.strip()
        if (title == site):
            print("SKIPPED")
            return
    '''

    article_data = soup.find("div", id="articleData")
    for data in article_data.find_all():
        if (data.has_attr("id")):
            if (data["id"] == "author"):
                author = data.text
                author = re.sub(r"\|", "", author)
                author = author.strip()
            elif (data["id"] == "storyDate"):
                story_date = data.text

    story_date = re.findall(r"(\S+)", story_date)

    for index in range(len(story_date)):
        story_date[index] = story_date[index].strip(",")
        if (index == 0):
            if (story_date[index] == "Jan"):
                story_date[index] = "01"
            elif (story_date[index] == "Feb"):
                story_date[index] = "02"
            elif (story_date[index] == "Mar"):
                story_date[index] = "03"
            elif (story_date[index] == "Apr"):
                story_date[index] = "04"
            elif (story_date[index] == "May"):
                story_date[index] = "05"
            elif (story_date[index] == "Jun"):
                story_date[index] = "06"
            elif (story_date[index] == "Jul"):
                story_date[index] = "07"
            elif (story_date[index] == "Aug"):
                story_date[index] = "08"
            elif (story_date[index] == "Sep"):
                story_date[index] = "09"
            elif (story_date[index] == "Oct"):
                story_date[index] = "10"
            elif (story_date[index] == "Nov"):
                story_date[index] = "11"
            elif (story_date[index] == "Dec"):
                story_date[index] = "12"
            
        if (index == 1):
            if (int(story_date[index]) < 10):
                story_date[index] = "0" + story_date[index]

    for entry in story_date:
        date += entry

    all_tags = soup.find("div", class_="groupings").text
    all_tags = all_tags.strip()

    tags = re.split(", ", all_tags)

    content = soup.find("div", id="story")

    errors, warnings, print_friendly_errors, error_line_string = find_errors(content)
    try:
        fix_all(content, errors)
    except:
        print("Skipping HTML cleanup")

    driver.get(article_page_url)

    ohio_login(driver)

    wait = WebDriverWait(driver, 10)

    rich_text_xpath = '//*[@id="cke_1_contents"]/iframe'
    rich_text_body_xpath = '/html/body'
    rich_text_source_xpath = '//*[@id="cke_12_label"]'
    rich_text_textarea_xpath = '//*[@id="cke_1_contents"]/textarea'
    title_xpath = "//*[@id='edit-title-0-value']"
    author_xpath = "//*[@id='edit-field-author-0-value']"
    date_xpath = "//*[@id='edit-field-publication-date-0-value-date']"
    tag_xpath = '//*[@id="edit-field-scripps-college-article-ta"]'
    page_location_xpath = '//*[@id="edit-page-location"]/summary'
    parent_page_xpath = '//*[@id="edit-parent-page"]'
    page_url_slug_xpath = '//*[@id="edit-slug"]'
    save_xpath = "//*[@id='edit-submit']"
    create_content_xpath = "//*[@id='edit-submit']"
    parent_page = "- News"
    first = True

    driver.find_element_by_xpath(page_location_xpath).click()

    element = Select(driver.find_element_by_xpath(parent_page_xpath))
    element.select_by_visible_text(parent_page)
    driver.find_element_by_xpath(page_url_slug_xpath).send_keys(title)

    if (title != ""):
        element = driver.find_element_by_xpath(title_xpath)
        element.send_keys(title)

    if (author != ""):
        element = driver.find_element_by_xpath(author_xpath)
        element.send_keys(author)
    if (date != ""):
        element = driver.find_element_by_xpath(date_xpath)
        element.send_keys(date)

    output = ""

    driver.switch_to.frame(driver.find_element_by_xpath(rich_text_xpath))

    image_index = 0

    for tag in content:
        if (tag.name == "img"):
            try:
                driver.switch_to.default_content()
            except:
                pass

            try:
                file_name, image_title, alt_text = download_image(received_url, content)
                tag.decompose()
            except:
                image_index += 1
                continue

            try:
                embed_image(driver, file_name, image_title, alt_text)
            except:
                image_index += 1
                continue
        else:
            try:
                driver.switch_to.frame(driver.find_element_by_xpath(rich_text_xpath))
            except:
                pass

            line = str(tag.encode("utf-8"))
            line = line.strip()

            # For JavaScript code in Drupal
            line = line.replace('"', '\\"')
            line = line.replace("\n", "")

            if (re.findall("^\s*$", line)):
                continue

            element = driver.find_element_by_xpath(rich_text_body_xpath)
            html_backup = element.get_attribute("innerHTML")

            html_backup = html_backup.replace(u"\xa0", u" ")
            html_backup = html_backup.replace(u"\xc2", u" ")
            html_backup = str(html_backup.encode("utf-8"))
            html_backup = html_backup.replace('"', '\\"')

            if (not re.findall("^\s*$", html_backup)):
                body_textarea_script = 'document.getElementsByTagName("body")[0].innerHTML="' + html_backup + line + '";'
                driver.execute_script(body_textarea_script)

    try:
        driver.switch_to.default_content()
    except:
        pass

    if len(tags) > 0:
        for tag in tags:
            element = Select(driver.find_element_by_xpath(tag_xpath))

            if (first == True):
                element.deselect_all()
                first = False

            element.select_by_visible_text(tag)

    element = driver.find_element_by_xpath(save_xpath)
    element.click()

    '''
    alert = driver.switch_to.alert
    alert.accept()

    element = driver.find_element_by_xpath(create_content_xpath)
    element.click()
    '''
