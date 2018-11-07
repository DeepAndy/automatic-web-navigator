from selenium import webdriver
from bs4 import BeautifulSoup
import HTMLParser
import StringIO
import re
from fix_html import *
import getpass
import time

def script_main(driver):
        source = driver.page_source.encode("ascii", "ignore")

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

	cofa_main_page = "https://webcms.ohio.edu/fine-arts/admin/content"
	cas_username_xpath = "//*[@id='username']"
	cas_password_xpath = "//*[@id='password']"
	cas_login_button_xpath = "/html/body/div[1]/div[2]/div/form/section[3]/div/button[1]"
	add_content_xpath = "//*[@id='block-seven-local-actions']/ul/li/a"
	basic_page_xpath = "//*[@id='block-seven-content']/ul/li[7]/a"
	body_textarea_script = 'document.getElementsByTagName("body")[0].innerHTML = "' + output + '"'

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

	element = driver.find_element_by_xpath(add_content_xpath)
	element.click()
	element = driver.find_element_by_xpath(basic_page_xpath)
	element.click()
	driver.execute_script(body_textarea_script)
