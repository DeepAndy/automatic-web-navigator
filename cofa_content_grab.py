from selenium import webdriver
from bs4 import BeautifulSoup
import HTMLParser
import StringIO
import re
from fix_html import *

def script_main(driver):
        source = driver.page_source
        source = source.replace("&nbsp;", "")

        soup = BeautifulSoup(source, features="html.parser")

        content = soup.find("div", id="cofa_contentCol1")

        for script in content.find_all("script"):
                script.decompose()

        for style in content.find_all("style"):
                style.decompose()

        for link in content.find_all("link"):
                link.decompose()

        content = HTMLParser().unescape(content)
        content = StringIO.StringIO(content)
        content = content.readlines()

        lines, errors, warnings, print_friendly_errors, error_line_string = find_errors(content)
        fix_all(lines, errors)
        
        output = ""

        for line in lines:
                output += line + "\n"

        print(output)
