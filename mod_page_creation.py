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
    
    title_xpath = "//*[@id='edit-title-0-value']"
    element = driver.find_element_by_xpath(title_xpath)
    title = element.get_attribute("value")

    mod_page_url = "https://webcms.ohio.edu/fine-arts/node/add/modular_page"

    driver.get(mod_page_url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    element = driver.find_element_by_xpath(title_xpath)
    element.send_keys(title)

    page_container_xpath = "//input[starts-with(@id, 'edit-field-page-container-add-more-add-more-button-page-content-row')]"
    explore_tabs_xpath = "//*[@value='Add Explore Tabs']"
    heading_tabs_xpath = '//input[starts-with(@id, "edit-field-page-container-0-subform-field-tab-0-subform-field-title-0-value")]'
    heading_value = "Explore Our Schools"
    # //*[@id="edit-field-page-container-0-subform-field-tab-0-subform-field-title-0-value--Xm0GhEaM_ac"]
    large_image_with_text_xpath = "//*[@value='Add Large Image with Text Callout']"
    page_container_button_first_xpath = '//*[@id="edit-field-page-container"]/div[3]/div/ul/li[2]/button'
    page_container_button_xpath = '//div/div[4]/div/div/ul/li[2]/button'
    content_column_button_xpath_one = "//div[starts-with(@id, 'edit-field-page-container-2-subform-field-columns-0-subform-field-modular-page-item')]/div[3]/div/ul/li[2]/button"
    content_text_editor_xpath = '//input[starts-with(@id, "edit-field-page-container-2-subform-field-columns-0-subform-field-modular-page-item-add-more-add-more-button-content-blurb-text-editor")]'
    text_format_xpath = '//select[starts-with(@id, "edit-field-page-container-2-subform-field-columns-0-subform-field-modular-page-item-0-subform-field-content-blurb-body-0-format")]'
    text_format = 'HTML Editor'
    editor_textarea_xpath = '//textarea[starts-with(@id, "edit-field-page-container-2-subform-field-columns-0-subform-field-modular-page-item-0-subform-field-content-blurb-body-0-value")]'
    # //*[@id="edit-field-page-container-2-subform-field-columns-0-subform-field-modular-page-item-0-subform-field-content-blurb-body-0-value--GyDrM2IqXGs"]
    content_column_button_xpath_two = '//div[starts-with(@id, "edit-field-page-container-3-subform-field-columns-0-subform-field-modular-page-item")]/div[3]/div/ul/li[2]/button'
    # //*[@id="edit-field-page-container-3-subform-field-columns-0-subform-field-modular-page-item--HxfdTQtMjAA"]/div[3]/div/ul/li[2]/button
    view_block_xpath = '//input[starts-with(@id, "edit-field-page-container-3-subform-field-columns-0-subform-field-modular-page-item-add-more-add-more-button-view-block")]'
    # //*[@id="edit-field-page-container-3-subform-field-columns-0-subform-field-modular-page-item-add-more-add-more-button-view-block--8WkfhmTY66E"]
    views_selection_xpath = '//input[starts-with(@id, "edit-field-page-container-3-subform-field-columns-0-subform-field-modular-page-item-0-subform-field-views-selection-0-target-id")]'
    # //*[@id="edit-field-page-container-3-subform-field-columns-0-subform-field-modular-page-item-0-subform-field-views-selection-0-target-id--XO1F1gNM6Dg"]
    display_settings_xpath = '//*[@id="edit-ds-switch-view-mode"]/summary'
    save_xpath = '//*[@id="edit-submit"]'
    column_xpath = '//*[@id="edit-column-number"]'
    column_number = '1'

    content_blurb_body = '<div class="text-center">\n<h2 class="display-three">Featured Events</h2>\n<a class="active-link" href="https://calendar.ohio.edu/site/finearts">View All Fine Arts Events</a>\n</div>\n\n<script>var $ = jQuery;</script>\n<script type="text/javascript" src="https://calendar.ohio.edu/Scripts/core.js"></script>\n<script type="text/javascript">\n    ActiveData.Events(\n        "https://calendar.ohio.edu/handlers/query.ashx?id=b6755bef8e8d43c3835ada93641e1772&tenant=&site=finearts",\n        function (response)\n{$("#c508f8dc20a04119a5b30069a0d77a31").append(response.data);}\n    );\n</script>\n<div class="container"><div id="c508f8dc20a04119a5b30069a0d77a31" class="row">\n</div></div>'
    views_selection = 'Fine Arts News (fine_arts_news)'
    
    # Set number of columns 
    element = driver.find_element_by_xpath(display_settings_xpath)
    element.click()
    element = Select(driver.find_element_by_xpath(column_xpath))
    element.select_by_visible_text(column_number)

    # Explore Tabs
    element = driver.find_element_by_xpath(page_container_button_first_xpath)
    element.click()
    element = driver.find_element_by_xpath(explore_tabs_xpath)
    element.click()
    # Fill out heading
    time.sleep(2)
    element = driver.find_element_by_xpath(heading_tabs_xpath)
    element.send_keys(heading_value)

    # Large Image with Text Callout
    time.sleep(2)
    element = driver.find_element_by_xpath(page_container_button_xpath)
    element.click()
    element = driver.find_element_by_xpath(large_image_with_text_xpath)
    element.click()

    # Page Content Row
    time.sleep(2)
    element = driver.find_element_by_xpath(page_container_button_xpath)
    element.click()
    element = driver.find_element_by_xpath(page_container_xpath)
    element.click()
    # Create content text editor
    time.sleep(2)
    element = driver.find_element_by_xpath(content_column_button_xpath_one)
    element.click()
    element = driver.find_element_by_xpath(content_text_editor_xpath)
    element.click()
    # Select HTML Editor
    time.sleep(2)
    element = Select(driver.find_element_by_xpath(text_format_xpath))
    element.select_by_visible_text(text_format)
    # Fill content text editor
    element = driver.find_element_by_xpath(editor_textarea_xpath)
    element.send_keys(content_blurb_body)

    # Page Content Row
    time.sleep(2)
    element = driver.find_element_by_xpath(page_container_button_xpath)
    element.click()
    element = driver.find_element_by_xpath(page_container_xpath)
    element.click()
    # View Block
    time.sleep(2)
    element = driver.find_element_by_xpath(content_column_button_xpath_two)
    element.click()
    element = driver.find_element_by_xpath(view_block_xpath)
    element.click()
    # View Selection
    time.sleep(2)
    element = driver.find_element_by_xpath(views_selection_xpath)
    element.send_keys(views_selection)

    element = driver.find_element_by_xpath(save_xpath)
    element.click()

    '''
    alert = driver.switch_to.alert
    alert.accept()

    time.sleep(0.5)
    '''
