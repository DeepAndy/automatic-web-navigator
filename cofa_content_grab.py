from selenium import webdriver
from bs4 import BeautifulSoup
import HTMLParser
import StringIO
import re
from fix_html import *
import getpass
import time
from pyexcel import *

def script_main(driver):
	f = open("failed_cofa_grab.txt", "a+")
	sheet = get_sheet(file_name="CoFA News.xlsx")
	school_names = sheet.column[2];
	urls = sheet.column[3];

	for i in range(len(urls)):
		if (urls[i] == driver.current_url):
			tag_name = school_names[i]

	# print(tag_name)

	source = driver.page_source.encode("ascii", "ignore")
	source = source.replace("&nbsp;", "")
	soup = BeautifulSoup(source, features="html.parser")

	try:
		content = soup.find("div", id="cofa_contentCol1")
	except:
			f.write(driver.current_url + "\n")

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

	title = soup.find_all("h1")[1].text

	output = ""

	for line in lines:
		line = line.strip()
		output += line

	output = re.sub(r"'", "\\'", output)

	cofa_main_page = "https://webcms.ohio.edu/fine-arts/admin/content"
	cas_username_xpath = "//*[@id='username']"
	cas_password_xpath = "//*[@id='password']"
	cas_login_button_xpath = "/html/body/div[1]/div[2]/div/form/section[3]/div/button[1]"
	basic_page_url = "https://webcms.ohio.edu/fine-arts/node/add/page"
	body_textarea_xpath = "//textarea[@data-editor-value-original]"
	body_textarea_script = "window.frames[0].document.getElementsByTagName('body')[0].innerHTML='" + output + "';"
	save_xpath = "//*[@id='edit-submit']"

	'''
	driver.get(cofa_main_page)

	if (re.findall(r"cas.sso.ohio.edu", str(driver.current_url))):
		username = raw_input("Enter OHIO username: ")
		password = getpass.getpass("Enter OHIO password: ")

		element = driver.find_element_by_xpath(cas_username_xpath)
		element.send_keys(username)
		element = driver.find_element_by_xpath(cas_password_xpath)
		element.send_keys(password)
		element = driver.find_element_by_xpath(cas_login_button_xpath)
		element.click()

	driver.get(basic_page_url)
	time.sleep(1) # NEED TO WAIT FOR TEXTAREA TO LOAD
	driver.execute_script(body_textarea_script)
	'''
