import urllib                                                                    
import re
import os
from bs4 import BeautifulSoup

'''
Author:         Austin Moore
Script Type:    Helper Script
Description:    Download and upload images to Drupal
'''

def download_image(url, content, image_index):
    content = str(content)
    soup = BeautifulSoup(content, features="html.parser")
    images = soup.find_all("img")
    main_url = re.findall(r"\//(.+?)/", url)[0]
    index = 0

    for image in images:
        if (index != image_index):
            index += 1
            continue
        else:
            # print(image)
            image_source = image["src"] 
            alt_text = image["alt"]
            file_name = re.findall(r"/([^/]+\.\w+)$", image_source)[0]
            image_title = re.findall(r"(.+?)\.", file_name)[0]

            if (alt_text == ""):
                alt_text = "No alternative text available"

            if (image_source.find("/") == 0):
                image_source = "https://" + main_url + image_source

            '''
            print("image_source = " + image_source)
            print("alt_text = " + alt_text)
            print("file_name = " + file_name)
            print("image_title = " + image_title)
            print("url = " + url)
            print("main_url = " + main_url)
            '''

            try:
                urllib.urlretrieve(image_source, "images/" + file_name)
            except:
                print("Failed to download image at \"" + image_source + "\"")

            break

    return image_title, alt_text
