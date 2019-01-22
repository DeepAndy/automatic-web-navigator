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
from fix_html import *
from ohio_login import ohio_login

def script_main(driver, received_url, pos):
    page_source = driver.page_source
    page_source = page_source.replace(u"\xa0", u" ")
    page_source = page_source.replace(u"\xc2", u" ")
    soup = BeautifulSoup(page_source, features="html.parser")

    title = ""
    author = ""
    story_date = ""
    date = ""

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
    fix_all(content, errors)

    title = driver.title

    cas_username_xpath = "//*[@id='username']"
    cas_password_xpath = "//*[@id='password']"
    cas_login_button_xpath = "/html/body/div[1]/div[2]/div/form/section[3]/div/button[1]"
    compare_page_url = "https://webcms.ohio.edu/group/461/nodes?status=All&type=article&combine="
    article_page_url = "https://webcms.ohio.edu/group/461/content/create/group_node%3Aarticle"

    output = ""

    for tag in content:
        line = str(tag.encode("utf-8"))
        line = line.strip()
        output += line

    output = re.sub(r"'", "\\'", output)
    output = re.sub(r"\n", "", output)

    driver.get(compare_page_url)

    ohio_login(driver)

    time.sleep(1) # NEED TO WAIT FOR TEXTAREA TO LOAD

    title_xpath = "//*[@id='edit-title-0-value']"
    author_xpath = "//*[@id='edit-field-author-0-value']"
    date_xpath = "//*[@id='edit-field-publication-date-0-value-date']"
    tag_xpath = '//*[@id="edit-field-scripps-college-article-ta"]'
    page_location_xpath = '//*[@id="edit-page-location"]/summary'
    parent_page_xpath = '//*[@id="edit-parent-page"]'
    page_url_slug_xpath = '//*[@id="edit-slug"]'
    #navigation_xpath = "//*[@id='edit-menu-parent']"
    #display_settings_xpath = "//*[@id='edit-ds-switch-view-mode']/summary"
    #column_xpath = "//*[@id='edit-column-number']"
    body_textarea_script = "window.frames[0].document.getElementsByTagName('body')[0].innerHTML='" + output + "';"
    save_xpath = "//*[@id='edit-submit']"
    create_content_xpath = "//*[@id='edit-submit']"
    parent_page = "- News"
    first = True

    driver.find_element_by_xpath(page_location_xpath).click()
    time.sleep(1)

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

    driver.execute_script(body_textarea_script)

    if len(tags) > 0:
        for tag in tags:
            element = Select(driver.find_element_by_xpath(tag_xpath))

            if (first == True):
                element.deselect_all()
                first = False

            element.select_by_visible_text(tag)

    time.sleep(10)
    '''
    element = driver.find_element_by_xpath(save_xpath)
    element.click()

    alert = driver.switch_to.alert
    alert.accept()

    element = driver.find_element_by_xpath(create_content_xpath)
    element.click()

    time.sleep(0.5)
    '''
