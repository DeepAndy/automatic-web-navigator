'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    This script finds all box and sharepoint links on Ohio
                University's Medicine site and outputs to an Excel file. Used
                in conjunction with navigator.py
Python 2.7.10
'''

import pyexcel
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def script_main(driver, url, pos):
    source = driver.page_source
    page_url = driver.current_url
    title = driver.title
    soup = BeautifulSoup(source, "html.parser")
    decommissioned = False
    page_not_found = False
    data = []

    for tag in soup.find_all("h1"):
        if (tag.text == "This page has been decommissioned"):
            decommissioned = True
        if (tag.text == "Aw, Nuts!"):
            page_not_found = True

    if (decommissioned == False and page_not_found == False):
        first_href = True
        box_links = []
        onedrive_links = []

        for tag in soup.find_all("a"):
            if (tag.has_attr("href")):
                if (re.findall("ohio.box.com", tag["href"]) and tag["href"].find("javascript") != 0):
                    box_links.append(tag["href"])
                if (re.findall("catmailohio.sharepoint.com", tag["href"])):
                    onedrive_links.append(tag["href"])

        if (len(box_links) >= len(onedrive_links)):
            end_of_loop = box_links
            larger = "box"
        else:
            end_of_loop = onedrive_links
            larger = "onedrive"

        for index in range(len(end_of_loop)):
            if (first_href == True):
                if (len(box_links) >= 1 and len(onedrive_links) >= 1):
                    data.append([title, page_url, box_links[0], onedrive_links[0]])
                elif (len(box_links) >= 1 and len(onedrive_links) == 0):
                    data.append([title, page_url, box_links[0], ''])
                elif (len(box_links) == 0 and len(onedrive_links) >= 1):
                    data.append([title, page_url, '', onedrive_links[0]])
                first_href = False
            else:
                if (larger == "box"):
                    if (index < len(box_links) and index < len(onedrive_links)):
                        data.append(['', '', box_links[index], onedrive_links[index]])
                    elif (index < len(box_links) and index >= len(onedrive_links)):
                        data.append(['', '', box_links[index], ''])
                    elif (index >= len(box_links) and index < len(onedrive_links)):
                        data.append(['', '', '', onedrive_links[index]])
                elif (larger == "onedrive"):
                    if (index < len(box_links) and index < len(onedrive_links)):
                        data.append(['', '', box_links[index], onedrive_links[index]])
                    elif (index < len(box_links) and index >= len(onedrive_links)):
                        data.append(['', '', box_links[index], ''])
                    elif (index >= len(box_links) and index < len(onedrive_links)):
                        data.append(['', '', '', onedrive_links[index]])

        sheet = pyexcel.get_sheet(file_name="example.xlsx")
        sheet.row += data
        sheet.save_as("example.xlsx")
    elif (decommissioned == True):
        print("DECOMISSIONED")
    elif (page_not_found == True):
        print("AW, NUTS!")
