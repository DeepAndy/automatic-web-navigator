import io
from selenium import webdriver
from ohio_login import ohio_login
from bs4 import BeautifulSoup

'''
Author:         Austin Moore
Script Type:    Main Script
Description:    Just a quick script to copy over already used Scripps page
                title. Some code is just hard-coded since this is a one time
                script.
'''

driver = webdriver.Chrome(executable_path="/Users/am058613/Desktop/chromedriver")

page = 0
first = False
f = io.open("title.txt", "w", encoding="utf-8")

while (page < 4):
    driver.get("https://webcms.ohio.edu/group/461/nodes?status=All&type=All&combine=&page=" + str(page))

    if (first == False):
        ohio_login(driver)
    else:
        first = True

    page_source = driver.page_source
    page_source = page_source.replace(u"\xa0", u" ")
    page_source = page_source.replace(u"\xc2", u" ")

    soup = BeautifulSoup(page_source, features="html.parser")

    for tag in soup.find_all("td", class_="views-field views-field-title"):
        for tag in soup.find_all("a"):
            if (tag.has_attr("href") and tag.has_attr("hreflang")):
                if (tag.text != "Edit node" and tag.text != "Delete node" and tag.text != "Remove from Group"):
                    f.write(tag.text + "\n")

    page += 1
