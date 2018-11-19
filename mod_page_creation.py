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

def script_main(driver, url):
	cas_username_xpath = "//*[@id='username']"
	cas_password_xpath = "//*[@id='password']"
	cas_login_button_xpath = "/html/body/div[1]/div[2]/div/form/section[3]/div/button[1]"

	if (re.findall(r"cas.sso.ohio.edu", str(driver.current_url))):
		username = raw_input("Enter OHIO username: ")
		password = getpass.getpass("Enter OHIO password: ")

		element = driver.find_element_by_xpath(cas_username_xpath)
		element.send_keys(username)
		element = driver.find_element_by_xpath(cas_password_xpath)
		element.send_keys(password)
		element = driver.find_element_by_xpath(cas_login_button_xpath)
		element.click()

	driver.get(url)
	
	title_xpath = "//*[@id='edit-title-0-value']"
	element = driver.find_element_by_xpath(title_xpath)
	title = element.get_attribute("value")

	mod_page_url = "https://webcms.ohio.edu/fine-arts/node/add/modular_page"

	driver.get(mod_page_url)
	soup = BeautifulSoup(driver.page_source, "html.parser")

	element = driver.find_element_by_xpath(title_xpath)
	element.send_keys(title)

	page_container_xpath = "//*[@id='edit-field-page-container-add-more-add-more-button-page-content-row']"
	explore_tabs_xpath = "//*[@value='Add Explore Tabs']"
	large_image_with_text_xpath = "//*[@value='Add Large Image with Text Callout']"
	page_container_button_first_xpath = '//*[@id="edit-field-page-container"]/div[3]/div/ul/li[2]/button'
	page_container_button_xpath = '//div/div[4]/div/div/ul/li[2]/button'
	#//*[@id="field-page-container-add-more-wrapper--CFZet-ihssg"]/div/div[4]/div/div/ul/li[2]/button
	# Explore, large image, advanced, advanced

	button = driver.find_element_by_xpath(page_container_button_first_xpath)
	button.click()

	element = driver.find_element_by_xpath(explore_tabs_xpath)
	element.click()

	time.sleep(1)
	button2 = driver.find_element_by_xpath(page_container_button_xpath)
	button2.click()

	element = driver.find_element_by_xpath(large_image_with_text_xpath)
	element.click()

	time.sleep(1)
	button2 = driver.find_element_by_xpath(page_container_button_xpath)
	button2.click()

	element = driver.find_element_by_xpath(page_container_xpath)
	element.click()

	time.sleep(1)
	button2 = driver.find_element_by_xpath(page_container_button_xpath)
	button2.click()

	element = driver.find_element_by_xpath(page_content_row_xpath)
	element.click()

	'''
	element = driver.find_element_by_xpath(save_xpath)
	element.click()

	alert = driver.switch_to.alert
	alert.accept()

	time.sleep(0.5)
	'''
