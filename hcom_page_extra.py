import re
import time
from bs4 import BeautifulSoup, Comment
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ohio_login import ohio_login
from fix_html import *
from download_image_document import *

def drupal_action(driver, url, soup):
    title = driver.title
    title = title.replace('"', '\\"')

    webcms_url = 'https://webcms.ohio.edu/medicine/group/1/content/create/group_node%3Aarticle'
    driver.get(webcms_url)
    ohio_login(driver)

    wait = WebDriverWait(driver, 30)

    # Set page title
    wait.until(EC.visibility_of_element_located((By.ID, 'edit-title-0-value')))
    driver.execute_script('document.getElementById("edit-title-0-value").value="' + title + '";')

    # Enter the value of the parent page
    driver.execute_script('document.getElementById("edit-page-location").getElementsByClassName("seven-details__summary")[0].click();')
    select = Select(driver.find_element_by_id('edit-parent-page'))
    select.select_by_visible_text('-- News')

    # Enter the title into the page url slug
    if (len(title) > 128):
        title = title[0:128]
    wait.until(EC.visibility_of_element_located((By.ID, 'edit-slug')))
    driver.execute_script('document.getElementById("edit-slug").value="' + title + '";')

    # Enter date
    date = '2006-01-01'
    wait.until(EC.visibility_of_element_located((By.ID, 'edit-field-publication-date-0-value-date')))
    driver.execute_script('document.getElementById("edit-field-publication-date-0-value-date").value="' + date + '";')

    # Click page location
    driver.execute_script('document.getElementsByClassName("seven-details__summary")[0].click();')

    # Click display settings
    wait.until(EC.visibility_of_element_located((By.ID, 'edit-ds-switch-view-mode')))
    driver.find_element_by_id('edit-ds-switch-view-mode').click()

    # Change number of columns
    wait.until(EC.visibility_of_element_located((By.ID, 'edit-column-number')))
    select = Select(driver.find_element_by_id('edit-column-number'))
    select.select_by_visible_text('1')

    # Change article type
    wait.until(EC.visibility_of_element_located((By.ID, 'edit-field-article-type')))
    select = Select(driver.find_element_by_id('edit-field-article-type'))
    select.select_by_visible_text('News')

    output = ''

    for index in range(len(soup.contents)):
        if (re.search('^\s*$', str(soup.contents[index]))):
            pass
        else:
            output += str(soup.contents[index])

    output = output.replace('"', '\\"')
    output = output.replace('\n', '')

    try:
        driver.execute_script('window.frames[1].document.getElementsByTagName("body")[0].innerHTML="' + output + '";')
    except Exception as e:
        print(e)

    driver.find_element_by_id('edit-submit').click()

    # Accept leave page alert
    try:
        driver.switch_to.alert.accept()
    except:
        pass

def script_main(driver, url, pos):
    #try:
    if (re.search(r'https?://www.ohio.edu/medicine/news-archive', driver.current_url)):
        print('CURRENT PAGE: ' + driver.current_url)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        soup = soup.find('table', attrs={'width': '90%'})
        print('90% WIDTH')

        if soup is None:
            soup = BeautifulSoup(page_source, 'html.parser')
            soup = soup.find('table', attrs={'width': '100%'})
            print('100% WIDTH')

        if soup is None:
            print('NO CONTENT FOUND')
            return

        unwraps = soup.find_all(['table', 'tbody', 'tr', 'td', 'font', 'body', 'html'])

        for tag in unwraps:
            tag.unwrap()

        for tag in soup.find_all():
            if (tag.has_attr('align')):
                del tag['align']

        comments = soup.find_all(text=lambda text:isinstance(text, Comment))

        for comment in comments:
            comment.extract()

        errors, warnings, print_friendly_errors, error_line_string = find_errors(soup)
        download_documents_from_soup(soup)
        html_cleaned = False

        try:
            soup = fix_all(soup, errors)
            html_cleaned = True
        except:
            print('Failed to cleanup HTML')

        if (html_cleaned == True):
            drupal_action(driver, url, soup)

    else:
        f1 = open('skipped.txt', 'a')
        f1.write(driver.current_url + '\n')
    '''
    except:
        print('FAILED TO SCRAPE CONTENT')
        f1 = open('skipped.txt', 'a')
        f1.write(driver.current_url + '\n')
    '''
