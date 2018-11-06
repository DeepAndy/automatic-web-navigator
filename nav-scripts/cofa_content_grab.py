from selenium import webdriver
import BeautifulSoup
from bs4 import BeautifulSoup
import HTMLParser
import StringIO
import re
from fix_html import *

url = raw_input("Enter URL: ")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path="/Users/am058613/Desktop/chromedriver", chrome_options = chrome_options)
driver.get(url)

source = driver.page_source

soup = BeautifulSoup(source, features="html.parser")
#print(soup.prettify())

content = soup.find_all("div", id="cofa_contentCol1")[0]

for script in content.find_all("script"):
	script.decompose()

for style in content.find_all("style"):
	style.decompose()

for link in content.find_all("link"):
	link.decompose()

content = HTMLParser().unescape(content)
content = StringIO.StringIO(content)
content = content.readlines()

for index in range(len(content)):
	content[index] = content[index].replace("\n", "")

lines, errors, warnings, print_friendly_errors, error_line_string = find_errors(content)
fix_all(lines, errors)

for line in lines:
	print(line)
