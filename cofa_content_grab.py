from selenium import webdriver
from bs4 import BeautifulSoup
import HTMLParser
import StringIO
import re
from fix_html import *
import getpass
import time
from pyexcel import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def script_main(driver):
	sheet = get_sheet(file_name="CoFA News.xlsx")
	school_names = sheet.column[2];
	urls = sheet.column[3];

	for i in range(len(urls)):
		if (urls[i] == driver.current_url):
			tag_name = school_names[i]

	tags = tag_name.split(",")

	page_source = driver.page_source
	page_source = page_source.replace(u"\xa0", u" ")
	page_source = page_source.replace(u"\xc2", u" ")
	soup = BeautifulSoup(page_source, features="html.parser")

	content = soup.find("div", id="story")

	if (str(content) == "None"):
		f.write(str(driver.current_url) + "\n")
		return

	errors, warnings, print_friendly_errors, error_line_string = find_errors(content)
	fix_all(content, errors)

	title = driver.title

	cas_username_xpath = "//*[@id='username']"
	cas_password_xpath = "//*[@id='password']"
	cas_login_button_xpath = "/html/body/div[1]/div[2]/div/form/section[3]/div/button[1]"
	article_page_url = "https://webcmsdev.oit.ohio.edu/fine-arts/node/add/article"
	first = True

	output = ""

	for tag in content:
		line = str(tag.encode("utf-8"))
		line = line.strip()
		output += line

	output = re.sub(r"'", "\\'", output)
	output = re.sub(r"\n", "", output)

	driver.get(article_page_url)

	if (re.findall(r"cas.sso.ohio.edu", str(driver.current_url))):
		username = raw_input("Enter OHIO username: ")
		password = getpass.getpass("Enter OHIO password: ")

		element = driver.find_element_by_xpath(cas_username_xpath)
		element.send_keys(username)
		element = driver.find_element_by_xpath(cas_password_xpath)
		element.send_keys(password)
		element = driver.find_element_by_xpath(cas_login_button_xpath)
		element.click()

	#driver.get(article_page_url)
	time.sleep(1) # NEED TO WAIT FOR TEXTAREA TO LOAD

	title_xpath = "//*[@id='edit-title-0-value']"
	select_xpath = "//*[@id='edit-field-fine-arts-news-tags']"
	body_textarea_xpath = "//textarea[@data-editor-value-original]"
	body_textarea_script = "window.frames[0].document.getElementsByTagName('body')[0].innerHTML='" + output + "';"
	save_xpath = "//*[@id='edit-submit']"


	element = driver.find_element_by_xpath(title_xpath)
	element.send_keys(title)
	
	driver.execute_script(body_textarea_script)
	
	for tag in tags:
		if (tag != "CoFA"):
			element = Select(driver.find_element_by_xpath(select_xpath))

			if (first == True):
				element.deselect_all()
				first = False

			element.select_by_visible_text('-' + tag)

	element = driver.find_element_by_xpath(save_xpath)
	element.click()

	alert = driver.switch_to.alert
	alert.accept()
