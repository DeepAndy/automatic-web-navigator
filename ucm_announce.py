from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import re
import getpass

def script_main(driver, url, pos):
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

    f = open("in-the-news-all.html")
    soup = BeautifulSoup(f.read(), "html.parser")

    for article in soup.find_all("article", id="newsItem-" + str(pos + 1)):
        for tag in article.find_all("div"):
            if (tag.has_attr("class")):
                if (tag["class"][0] == "title"):
                    title = tag.text
                elif (tag["class"][0] == "storyLink"):
                    storyLink = tag.text
                elif (tag["class"][0] == "source"):
                    source = tag.text
                elif (tag["class"][0] == "date"):
                    date = ""
                    tmp_date = tag.text
                    tmp_date = tmp_date.split('-')
                    date += tmp_date[1] + tmp_date[2] + tmp_date[0]
                elif (tag["class"][0] == "newsID"):
                    newsID = "/ucm/in-the-news/" + tag.text

    title_xpath = '//*[@id="edit-title-0-value"]'
    storyLink_xpath = '//*[@id="edit-field-annc-link-0-uri"]'
    source_xpath = '//*[@id="edit-field-annc-source-0-value"]'
    date_xpath = '//*[@id="edit-field-annc-start-date-0-value-date"]'
    time_xpath = '//*[@id="edit-field-annc-start-date-0-value-time"]'
    url_path_xpath = '//*[@id="edit-path-settings"]/summary'
    url_alias_xpath = '//*[@id="edit-path-0-alias"]'
    save_xpath = '//*[@id="edit-submit"]'
    create_content_xpath = '//*[@id="edit-submit"]'
    link_yes_xpath = '//*[@id="edit-field-annc-link-check-1"]'

    driver.find_element_by_xpath(url_path_xpath).click()
    driver.find_element_by_xpath(url_alias_xpath).send_keys(newsID)
    driver.find_element_by_xpath(link_yes_xpath).click()
    driver.find_element_by_xpath(title_xpath).send_keys(title)
    driver.find_element_by_xpath(storyLink_xpath).send_keys(storyLink)
    driver.find_element_by_xpath(source_xpath).send_keys(source)
    driver.find_element_by_xpath(date_xpath).send_keys(date)
    driver.find_element_by_xpath(time_xpath).send_keys("120000a")

    driver.find_element_by_xpath(save_xpath).click()

    alert = driver.switch_to.alert
    alert.accept()

    driver.find_element_by_xpath(create_content_xpath).click()

