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

	f1 = open("write_out.html", "w+")

	for i in range(len(urls)):
		if (urls[i] == driver.current_url):
			tag_name = school_names[i]

	page_source = driver.page_source
	page_source = page_source.replace(u"\xa0", u"")
	page_source = page_source.replace(u"\xc2", u"")
	soup = BeautifulSoup(page_source, features="html.parser")

	content = soup.find("div", id="story")

	if (str(content) == "None"):
		f.write(str(driver.current_url) + "\n")
		return

	errors, warnings, print_friendly_errors, error_line_string = find_errors(content)
	fix_all(content, errors)

	title = soup.find_all("h1")[1].text

	cofa_main_page = "https://webcms.ohio.edu/fine-arts/admin/content"
	cas_username_xpath = "//*[@id='username']"
	cas_password_xpath = "//*[@id='password']"
	cas_login_button_xpath = "/html/body/div[1]/div[2]/div/form/section[3]/div/button[1]"
	basic_page_url = "https://webcms.ohio.edu/fine-arts/node/add/page"
	body_textarea_xpath = "//textarea[@data-editor-value-original]"
	body_textarea_script = "window.frames[0].document.getElementsByTagName('body')[0].innerHTML='" + soup.text + "';"
	save_xpath = "//*[@id='edit-submit']"

	output = ""

	for tag in content:
		line = str(tag.encode("utf-8"))
		line.strip()
		output += line

	#f1.write(output)

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
