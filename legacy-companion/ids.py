'''
Author:         Austin Moore
Script Type:    Companion Script
Description:    Print page source of Scripps pages to HTML files
Python 3.7.2
'''

import re

def script_main(driver, url, pos):
    page_source = driver.page_source
    title = driver.title

    title = title.lower()
    title = title.replace(" ", "-")
    title = title.replace("_", "-")
    title = re.sub(r"[^A-Za-z0-9\-]", "", title)
    f = open("html_files/" + title + ".html", "w")
    f.write(str(page_source))
