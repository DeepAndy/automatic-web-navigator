'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    This will take Drupal nodes as input and clean the HTML given
                in any rich text editor. Used in conjunction with navigator.py
Python 2.7.10
'''

import re
from bs4 import BeautifulSoup
from ohio_login import ohio_login

def script_main(driver, url, pos):
    ohio_login(driver)
    driver.get(url)

    page_source = driver.page_source
    page_source = page_source.replace(u"\xa0", u"")
    page_source = page_source.replace(u"\xc2", u"")
    soup = BeautifulSoup(page_source, features="html.parser")

    for tag in soup.find_all("iframe", {"class": "cke_wysiwyg_frame cke_reset"}):
        print(tag)
