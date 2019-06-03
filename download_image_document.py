import re
import urllib.request
from bs4 import BeautifulSoup

'''
Function:       download_image
Description:    Download an image from a string link
Parameters:     image (string)
'''
def download_image(image):
    try:
        file_name = re.search(r'\..*/(\S+\.\w+)', image).group(1)
    except:
        pass

    try:
        urllib.request.urlretrieve(image, "images/" + file_name)
        print('Successfully downloaded ' + file_name)
    except Exception as e:
        print("Failed to download image at \"" + image + "\"")
        print(e)
'''
Function:       download_document
Description:    Download a document from a string link
Parameters:     document (string)
'''
def download_document(document):
    try:
        file_name = re.search(r'\..*/(\S+\.\w+)', document).group(1)
    except:
        pass

    try:
        urllib.request.urlretrieve(document, "documents/" + file_name)
        print('Successfully downloaded ' + file_name)
    except Exception as e:
        print("Failed to download document at \"" + document + "\"")
        print(e)

'''
Function:       download_images_from_soup
Description:    Download images from a BeautifulSoup object
Parameters:     soup (BeautifulSoup object), url (Optional string), return_images (Optional bool)
Returns:        images (List of BeautifulSoup tags) (optional)
'''
def download_images_from_soup(soup, url='', return_images=False):
    images = soup.find_all('img', src=True)

    for image in images:
        if (re.search('^\s*$', url)):
            if (image['src'].find('/') == 0):
                image['src'] = 'https://www.ohio.edu' + image['src']

        download_image(image['src'])

    if (return_images == True):
        return images

'''
Function:       download_documents_from_soup
Description:    Download documents from a BeautifulSoup object
Parameters:     soup (BeautifulSoup object), url (Optional string)
'''
def download_documents_from_soup(soup, url=''):
    links = soup.find_all('a', href=True)
    documents = []

    for link in links:
        if (re.search('r(\.docx?)|(\.pptx?)|(\.xlsx?)|(\.pdf)|(\.zip)', link['href'])):
            if (re.search(r'^\s*$', url)):
                if (link['href'].find('/') == 0):
                    link['href'] = 'https://www.ohio.edu' + link['href']

            documents.append(link['href'])

    for document in documents:
        download_document(document)

'''
Function:       download_images_from_url
Description:    Download images from a given URL
Parameters:     url (string)
'''
def download_images_from_url(url):
    page_source = urllib.request.urlopen(url)
    page_source = page_source.read()
    soup = BeautifulSoup(page_source, 'html.parser')
    download_images_from_soup(soup)

'''
Function:       download_documents_from_url
Description:    Download documents from a given URL
Parameters:     url (string)
'''
def download_documents_from_url(url):
    page_source = urllib.request.urlopen(url)
    page_source = page_source.read()
    soup = BeautifulSoup(page_source, 'html.parser')
    download_documents_from_soup(soup)
