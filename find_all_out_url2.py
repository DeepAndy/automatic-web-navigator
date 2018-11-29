import pyexcel
import re
from bs4 import BeautifulSoup
from selenium import webdriver

def script_main(driver, url, pos):
    source = driver.page_source
    page_url = driver.current_url
    title = driver.title
    soup = BeautifulSoup(source, "html.parser")
    decomissioned = False
    data = []

    for tag in soup.find_all("h1"):
        if (tag.text == "This page has been decommissioned"):
            decomissioned = True

    if (decomissioned == False):
        first_href = True
        box_links = []
        onedrive_links = []

        for tag in soup.find_all("a"):
            if (tag.has_attr("href")):
                if (re.findall("ohio.box.com", tag["href"]) and not re.findall("javascript", tag["href"])):
                    box_links.append(tag["href"])
                if (re.findall("catmailohio.sharepoint.com", tag["href"])):
                    onedrive_links.append(tag["href"])

        if (first_href == True):
            if (len(box_links) >= 1 and len(onedrive_links) >= 1):
                data.append([title, page_url, box_links[0], onedrive_links[0]])
            elif (len(box_links) >= 1 and len(onedrive_links) == 0):
                data.append([title, page_url, box_links[0], ''])
            elif (len(box_links) == 0 and len(onedrive_links) >= 1):
                data.append([title, page_url, '', onedrive_links[0]])
            first_href = False
        else:
            if (len(box_links) >= len(onedrive_links)):
                for index in range(1, len(box_links)):
                    if (index < len(box_links) and index < len(onedrive_links)):
                        data.append(['', '', box_links[index], onedrive_links[index]])
                    elif (index < len(box_links) and index >= len(onedrive_links)):
                        data.append(['', '', box_links[index], ''])
                    elif (index >= len(box_links) and index < len(onedrive_links)):
                        data.append(['', '', '', onedrive_links[index]])
            else:
                for index in range(1, len(onedrive_links)):
                    if (index < len(box_links) and index < len(onedrive_links)):
                        data.append(['', '', box_links[index], onedrive_links[index]])
                    elif (index < len(box_links) and index >= len(onedrive_links)):
                        data.append(['', '', box_links[index], ''])
                    elif (index >= len(box_links) and index < len(onedrive_links)):
                        data.append(['', '', '', onedrive_links[index]])

        print(data)
    else:
        print("DECOMISSIONED")
