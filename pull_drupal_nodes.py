'''
Author:         Austin Moore
Script Type:    Main Script
Description:    This script is used to create a website queue (.wq) of nodes
                on Drupal
'''

import re
import ConfigParser
from selenium import webdriver
from collections import OrderedDict
import getpass
from bs4 import BeautifulSoup

class web_driver:
    def __init__(self, driver_type, driver_path):
        self.driver_type = driver_type
        self.driver_path = driver_path

class options:
    def __init__(self, remove_absolute, remove_current_page, remove_duplicates):
        self.remove_absolute = remove_absolute
        self.remove_current_page = remove_current_page
        self.remove_duplicates = remove_duplicates

def initialization():
    config = ConfigParser.ConfigParser()
    config_file = "config.ini"
    complete_config = True

    try:
        config.read(config_file)
    except:
        print
        print("Could not find the configuration file \"" + config_file + "\" or the file has no sections")
        print
        quit()

    found_driver_section = False
    found_pull_urls_section = False
    driver_section = "Driver"
    pull_urls_section = "pull-urls"

    for section in config.sections():
        if (section == driver_section):
            found_driver_section = True

        if (section == pull_urls_section):
            found_pull_urls_section = True

    if (found_driver_section == False):
        print
        print("Could not find the \"" + driver_section + "\" section.")
        print("Make sure a \"[" + driver_section + "]\" section is included in \"" + config_file + "\".")
        print
        quit()

    if (found_pull_urls_section == False):
        print
        print("Could not find the \"" + pull_urls_section + "\" section.")
        print("Make sure a \"[" + pull_urls_section + "]\" section is included in \"" + config_file + "\".")
        print
        quit()

    driver_option_type = "driver_type"
    driver_option_path = "driver_path"
    pull_urls_option_absolute = "remove_absolute"
    pull_urls_option_current_page = "remove_current_page"
    pull_urls_option_duplicates = "remove_duplicates"
    found_driver_type = False
    found_correct_driver_type = False
    found_driver_path = False
    found_pull_urls_absolute = False
    found_pull_urls_current_page = False
    found_pull_urls_duplicates = False
    pull_urls_remove_absolute = False
    pull_urls_remove_current_page = False
    pull_urls_remove_duplicates = False

    for option in config.options(driver_section):
        if (option == driver_option_type):
            found_driver_type = True

            if (config.get(driver_section, driver_option_type) == "chrome" or config.get(driver_section, driver_option_type) == "firefox"):
                found_correct_driver_type = True
                driver_type = config.get(driver_section, driver_option_type)

        if (option == driver_option_path):
            found_driver_path = True
            driver_path = config.get(driver_section, driver_option_path)

    if (found_driver_type == False):
        print
        print("Could not find the \"" + driver_option_type + "\" option is included under the \"[" + driver_section + "]\" section.")
        complete_config = False

    if (found_correct_driver_type == False):
        print
        print("The \"" + driver_option_type + "\" value is either incorrect or the option is missing.")
        print("Make sure the value is a valid option.")
        complete_config = False

    if (found_driver_path == False):
        print
        print("Could not find the \"" + driver_option_path + "\" option.")
        print("Make sure \"" + driver_option_path + "\" option is included under the \"[" + driver_section + "]\" section.")
        complete_config = False

    for option in config.options(pull_urls_section):
        if (option == pull_urls_option_absolute):
            found_pull_urls_absolute = True
            if (config.get(pull_urls_section, pull_urls_option_absolute) == "true"):
                pull_urls_remove_absolute = True

        if (option == pull_urls_option_current_page):
            found_pull_urls_current_page = True
            if (config.get(pull_urls_section, pull_urls_option_current_page) == "true"):
                pull_urls_remove_current_page = True

        if (option == pull_urls_option_duplicates):
            found_pull_urls_duplicates = True
            if (config.get(pull_urls_section, pull_urls_option_duplicates) == "true"):
                pull_urls_remove_duplicates = True

    if (found_pull_urls_absolute == False):
        print
        print("Could not find the \"" + pull_urls_option_absolute + "\" option.")
        print("Make sure \"" + pull_urls_option_absolute + "\" is included under the \"[" + pull_urls_section + "]\" section.")
        complete_config = False

    if (found_pull_urls_current_page == False):
        print
        print("Could not find the \"" + pull_urls_option_current_page + "\" option.")
        print("Make sure \"" + pull_urls_option_current_page + "\" is included under the \"[" + pull_urls_section + "]\" section.")
        complete_config = False

    if (found_pull_urls_duplicates == False):
        print
        print("Could not find the \"" + pull_urls_option_duplicates + "\" option.")
        print("Make sure \"" + pull_urls_option_duplicates + "\" is included under the \"[" + pull_urls_section + "]\" section.")
        complete_config = False

    if (complete_config == False):
        print
        quit()
    else:
        the_driver = web_driver(driver_type, driver_path)
        pull_urls_config = options(pull_urls_remove_absolute, pull_urls_remove_current_page, pull_urls_remove_duplicates)

    main(the_driver, pull_urls_config)

def select_urls(urls):
    lower = 0
    upper = 0
    exists = False
    print

    for index in range(len(urls)):
        url = urls[index]
        print("Website[" + str(index + 1) + "]: " + url)

    complete = False

    while (complete == False):
        print
        url_input = raw_input("Enter individual sites to add or specify a range: ")
        input_list = re.split(r' ', url_input)
        url_list = []

        for input_url in input_list:
            if (re.findall(r'\d+-\d+', input_url)):
                url_list.append(input_url)
            else:
                try:
                    url_list.append(int(input_url))
                except:
                    print
                    print("Incorrect input.")
                    continue

        complete = True

    option = ""

    while (option == ""):
        print
        output_file = raw_input("Enter a file name to write to: ")
        output_file = "web-queues/" + output_file + ".wq"

        try:
            open(output_file)
            exists = True
        except:
            f = open(output_file, "w+")
            break

        if (exists == True):
            print
            print("A file of that name already exists")
            print
            print("Would you like to: ")
            print("1. Append to file")
            print("2. Overwrite")
            print("3. Specify different name")
            print("4. Quit")
            print
            option = int(raw_input("Enter a number: "))

            if (option == 1):
                f = open(output_file, "a+")
            elif (option == 2):
                f = open(output_file, "w+")
            elif (option == 3):
                option = ""
                continue
            else:
                quit()

    for url in url_list:
        if (isinstance(url, int)):
            f.write(urls[url - 1] + "\n")
        else:
            numbers = re.split(r'-', url)
            lower = int(numbers[0])
            upper = int(numbers[1])

            for index in range(lower - 1, upper):
                f.write(urls[index] + "\n")

    print
    print("Wrote output to \"" + output_file + "\"")
    print

def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

def main(the_driver, pull_urls_config):
    if (the_driver.driver_type == "chrome"):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")

        try:
            driver = webdriver.Chrome(executable_path=the_driver.driver_path, chrome_options = chrome_options)
        except:
            print
            print("Could not open the chromedriver")
            print("Check that the driver type and driver path is correct in config.ini")
            print("These are the current driver settings:")
            print
            print("driver_type = " + the_driver.driver_type)
            print("driver_path = " + the_driver.driver_path)
            print
            quit()

    elif (the_driver.driver_type == "firefox"):
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")
        try:
            driver = webdriver.Firefox(executable_path=the_driver.driver_path, firefox_options = firefox_options)
        except:
            print
            print("Could not open the geckodriver")
            print("Check that the driver type and driver path is correct in config.ini")
            print("These are the current driver settings:")
            print
            print("driver_type = " + the_driver.driver_type)
            print("driver_path = " + the_driver.driver_path)
            print
            quit()

    print
    url = raw_input("Enter page to parse: ")
    driver.get(url)

    cas_username_xpath = "//*[@id='username']"
    cas_password_xpath = "//*[@id='password']"
    cas_login_button_xpath = "/html/body/div[1]/div[2]/div/form/section[3]/div/button[1]"
    article_page_url = "https://webcmsdev.oit.ohio.edu/fine-arts/node/add/article"

    if (re.findall(r"cas.sso.ohio.edu", str(driver.current_url))):
        username = raw_input("Enter OHIO username: ")
        password = getpass.getpass("Enter OHIO password: ")

        element = driver.find_element_by_xpath(cas_username_xpath)
        element.send_keys(username)
        element = driver.find_element_by_xpath(cas_password_xpath)
        element.send_keys(password)
        element = driver.find_element_by_xpath(cas_login_button_xpath)
        element.click()

    urls = []
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all("a"):
        if (tag.has_attr("href")):
            if (re.findall(r"edit\?destination=/", tag["href"])):
                urls.append(tag["href"])

    if (url.find(".com") != -1):
        new_url = re.split(r'\.com', url)[0] + ".com"
    elif (url.find(".org") != -1):
        new_url = re.split(r'\.org', url)[0] + ".org"
    elif (url.find(".edu") != -1):
        new_url = re.split(r'\.edu', url)[0] + ".edu"
    elif (url.find(".gov") != -1):
        new_url = re.split(r'\.gov', url)[0] + ".gov"
    elif (url.find(".net") != -1):
        new_url = re.split(r'\.net', url)[0] + ".net"
    elif (url.find(".html") != -1):
        new_url = re.split(r'\.html', url)[0] + ".html"

    for index in range(len(urls)):
        if (urls[index].find("/") == 0):
            urls[index] = new_url + urls[index]
        elif (urls[index].find("http://") == -1 and urls[index].find("https://") == -1 and urls [index].find("www.") == -1 and urls[index].find("file://") == -1):
            if (re.findall(r'(.*?)/[\w+|-]+\.\w+$', url)):
                new_url = re.findall(r'(.*?)/[\w+|-]+\.\w+$', url)[0]
                urls[index] = new_url + "/" + urls[index]

    select_urls(urls)

initialization()
