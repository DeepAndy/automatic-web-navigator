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
from fix_html import *
from ohio_login import ohio_login
from drupal_image import download_image

def script_main(driver, received_url, pos):
    page_source = driver.page_source
    page_source = page_source.replace(u"\xa0", u" ")
    page_source = page_source.replace(u"\xc2", u" ")
    soup = BeautifulSoup(page_source, features="html.parser")
    article_page_url = "https://webcmsdev.oit.ohio.edu/group/461/content/create/group_node%3Apage"

    title = ""
    author = ""
    story_date = ""
    date = ""

    title = driver.title

    print("title = " + title)

    f = io.open("title.txt", "r", encoding="utf-8")
    all_sites = f.readlines()

    for site in all_sites:
        site = site.strip()
        if (title == site):
            print("SKIPPED")
            return

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

    output = ""

    image_index = 0

    for tag in content:
        line = str(tag.encode("utf-8"))
        line = line.strip()
        if (tag == "img"):
            download_image(received_url, content, image_index)
            image_index += 1

        errors = []

        try:
            fix_all(line, errors)
        except:
            print("Skipping HTML cleanup")

        output += line

    # For JavaScript code in Drupal
    output = re.sub(r"'", "\\'", output)
    output = re.sub(r"\n", "", output)

    driver.get(article_page_url)

    ohio_login(driver)

    time.sleep(2) # NEED TO WAIT FOR TEXTAREA TO LOAD

    title_xpath = "//*[@id='edit-title-0-value']"
    author_xpath = "//*[@id='edit-field-author-0-value']"
    date_xpath = "//*[@id='edit-field-publication-date-0-value-date']"
    tag_xpath = '//*[@id="edit-field-scripps-college-article-ta"]'
    page_location_xpath = '//*[@id="edit-page-location"]/summary'
    parent_page_xpath = '//*[@id="edit-parent-page"]'
    page_url_slug_xpath = '//*[@id="edit-slug"]'
    body_textarea_script = "window.frames[0].document.getElementsByTagName('body')[0].innerHTML='" + output + "';"
    save_xpath = "//*[@id='edit-submit']"
    create_content_xpath = "//*[@id='edit-submit']"
    parent_page = "- News"
    first = True

    '''
    driver.find_element_by_xpath(page_location_xpath).click()
    time.sleep(2)

    element = Select(driver.find_element_by_xpath(parent_page_xpath))
    element.select_by_visible_text(parent_page)
    driver.find_element_by_xpath(page_url_slug_xpath).send_keys(title)
    '''

    if (title != ""):
        element = driver.find_element_by_xpath(title_xpath)
        element.send_keys(title)

    '''
    if (author != ""):
        element = driver.find_element_by_xpath(author_xpath)
        element.send_keys(author)
    if (date != ""):
        element = driver.find_element_by_xpath(date_xpath)
        element.send_keys(date)
    '''

    driver.execute_script(body_textarea_script)

    time.sleep(30)

    '''
    if len(tags) > 0:
        for tag in tags:
            element = Select(driver.find_element_by_xpath(tag_xpath))

            if (first == True):
                element.deselect_all()
                first = False

            element.select_by_visible_text(tag)

    element = driver.find_element_by_xpath(save_xpath)
    element.click()

    alert = driver.switch_to.alert
    alert.accept()

    element = driver.find_element_by_xpath(create_content_xpath)
    element.click()

    time.sleep(0.5)
    '''
