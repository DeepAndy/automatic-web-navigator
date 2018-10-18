import re
import ConfigParser
from selenium import webdriver

class web_driver:
    def __init__(self, driver_type, driver_path):
        self.driver_type = driver_type
        self.driver_path = driver_path

class options:
    def __init__(self, remove_absolute, remove_current_page):
        self.remove_absolute = remove_absolute
        self.remove_current_page = remove_current_page

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
    found_driver_type = False
    found_correct_driver_type = False
    found_driver_path = False
    found_pull_urls_absolute = False
    found_pull_urls_current_page = False

    for option in config.options(driver_section):
        if (option == driver_option_type):
            found_driver_type = True
            
            if (config.get(driver_section, driver_option_type) == "chrome"):
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
            else:
                pull_urls_remove_absolute = False

        if (option == pull_urls_option_current_page):
            found_pull_urls_current_page = True
            if (config.get(pull_urls_section, pull_urls_option_current_page) == "true"):
                pull_urls_remove_current_page = True
            else:
                pull_urls_remove_current_page = False

    if (found_pull_urls_absolute == False):
        print
        print("Could not find the \"" + pull_urls_option_absolute + "\" option.")
        print("Make sure \"" + pull_urls_option_absolute + "\" is included under the \"[" + pull_urls_section + "]\" section.")
    if (found_pull_urls_current_page == False):
        print
        print("Could not find the \"" + pull_urls_option_current_page + "\" option.")
        print("Make sure \"" + pull_urls_option_current_page + "\" is included under the \"[" + pull_urls_section + "]\" section.")

    if (complete_config == False):
        print
        quit()
    else:
        the_driver = web_driver(driver_type, driver_path)
        pull_urls_config = options(pull_urls_remove_absolute, pull_urls_remove_current_page)

    main(the_driver, pull_urls_config)

def select_urls(urls):
    lower = 0
    upper = 0
    exists = False
    print
    
    for index in range(len(urls)):
        url = urls[index]
        print("Website[" + str(index + 1) + "]: " + url)

    print
    url_input = raw_input("Enter individual sites to add or specify a range: ")
    url_list = re.split(r' ', url_input)
    
    if (len(url_list) == 1 and url_list[0].find("-") != -1):
        lower = int(re.findall(r'(\d+)-', url_list[0])[0])
        upper = int(re.findall(r'-(\d+)', url_list[0])[0])

    option = ""
    while (option == ""):
        print
        output_file = raw_input("Enter a file name to write to: ")
        output_file += ".wq"
    
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

    if (lower == 0 and upper == 0):
        for index in url_list:
            f.write(urls[int(index) - 1] + "\n")
    else:
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
        driver = webdriver.Chrome(executable_path=the_driver.driver_path, chrome_options = chrome_options)
    
    print
    url = raw_input("Enter page to parse: ")
    driver.get(url)
    html = driver.page_source
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', html)
    url_current_length = len(urls)

    # Remove anything that does not look like an actual URL
    for current_url in urls:
        if (current_url.find("http://") == -1 and current_url.find("https://") == -1):
            if (current_url.find(".com") == -1 and current_url.find(".org") == -1 and current_url.find(".edu") == -1 and current_url.find(".gov") == -1 and current_url.find(".net") == -1 and current_url.find(".html") == -1):
                if (current_url.find("/") != 0):
                    urls = remove_values_from_list(urls, current_url)
                    
        if (current_url.find("mailto:") == 0):
            urls = remove_values_from_list(urls, current_url)

    if (pull_urls_config.remove_absolute == True):
        for current_url in urls:
            if (current_url.find("/") == 0):
                urls = remove_values_from_list(urls, current_url)
    else:
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

    if (pull_urls_config.remove_current_page == True):
        urls = remove_values_from_list(urls, "#")
        urls = remove_values_from_list(urls, "/")
        urls = remove_values_from_list(urls, "\\")
        urls = remove_values_from_list(urls, url)

    select_urls(urls)

initialization()