'''
Author:         Austin Moore
Script Type:    Main Script
Description:    Used to make a website queue for CAS
Python 2.7.10
'''

import re
from bs4 import BeautifulSoup
from selenium import webdriver
from ohio_login import ohio_login

f = open("web-queues/cassites.wq", "a+")

driver = webdriver.Chrome(executable_path="/Users/am058613/Desktop/chromedriver")
url = raw_input("Enter Drupal page: ")
driver.get(url)

ohio_login(driver)

page_source = driver.page_source
page_source = page_source.replace(u"\xa0", u" ")
page_source = page_source.replace(u"\xc2", u" ")
soup = BeautifulSoup(page_source, features="html.parser")
append = "https://webcmsdev.oit.ohio.edu"

for tag in soup.find_all("td", {"headers": "view-dropbutton-table-column"}):
    for tag2 in tag.find_all("a", href=True):
        if (re.findall(r"/cas/node/\d+/edit\.*?", tag2["href"])):
            f.write(append + tag2["href"] + "\n")
