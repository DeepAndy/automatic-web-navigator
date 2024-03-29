import re
import os
import urllib.request
from bs4 import BeautifulSoup

'''
Function:       get_base_and_relative
Description:    Get the base URL and relative URL
Parameters:     url (string)
Returns:        base_url (string), relative_url (string)
Notes:          The returned URLs will have a '/' attached to the end
'''
def get_base_and_relative(url):
    if (url.find('file:///') == 0):
        base_url = re.compile(r'\S+/(\S+\.\w+)')
        base_url = re.search(base_url, url).group(1)
        base_url = re.sub(base_url, '', url)
    else:
        base_url = re.compile(r'\.\w+(/\S+)')
        base_url = re.search(base_url, url).group(1)
        base_url = re.sub(base_url, '', url)

    if (base_url[len(base_url) - 1] != '/'):
        base_url += '/'

    relative_url = re.sub(r'[^/]+$', '', url)

    if (relative_url[len(relative_url) - 1] != '/'):
        relative_url += '/'

    return base_url, relative_url

'''
Function:       create_url_from_relative
Description:    Creates a new download URL when the given href is a relative
                link
Parameters:     href (string), base_url (string), relative_url(string)
Returns:        href (string)
'''
def create_url_from_relative(href, base_url, relative_url):
    if (href.find('/') == 0):
        href = href[1:]
        href = base_url + href
    else:
        href = relative_url + href

    return href

'''
Function:       download_image
Description:    Download an image from a string link
Parameters:     image (string)
'''
def download_image(image):
    try:
        file_name = re.search(r'[^/]+\.((png)|(gif)|(jpe?g)|(jpe)|(jif)|(jfif?)|(svg)|(tiff?))', image, re.IGNORECASE).group(0)
        file_name = 'images/' + file_name
        i = 0

        while (os.path.isfile(file_name)):
            if (re.search(r'(\(\d+\))\.', file_name)):
                file_name = re.sub(r'(\(\d+\))', '', file_name)

            i += 1
            dot_index = file_name.find('.')
            file_name = file_name[:dot_index] + '(' + str(i) + ')' + file_name[dot_index:]
    except Exception as e:
        print('\nFailed to download image at "' + image + '"')
        print('This was a naming error')
        print(str(e) + '\n')
        return

    try:
        urllib.request.urlretrieve(image, file_name)
        print('Successfully downloaded /' + file_name)
    except Exception as e:
        print("\nFailed to download image at \"" + image + "\"")
        print(str(e) + '\n')
        return

'''
Function:       download_document
Description:    Download a document from a string link
Parameters:     document (string)
'''
def download_document(document):
    try:
        file_name = re.search(r'[^/]+\.((pdf)|(docx?)|(xlsx?)|(pptx?))', document, re.IGNORECASE).group(0)
        file_name = 'documents/' + file_name
        i = 0

        while (os.path.isfile(file_name)):
            if (re.search(r'(\(\d+\))\.', file_name)):
                file_name = re.sub(r'(\(\d+\))', '', file_name)

            i += 1
            dot_index = file_name.find('.')
            file_name = file_name[:dot_index] + '(' + str(i) + ')' + file_name[dot_index:]

    except Exception as e:
        print('\nFailed to download document at "' + document + '"')
        print('This was a naming error')
        print(str(e) + '\n')
        return

    try:
        urllib.request.urlretrieve(document, file_name)
        print('Successfully downloaded /' + file_name)
    except Exception as e:
        print('\nFailed to download document at "' + document + '"')
        print(str(e) + '\n')
        return

'''
Function:       download_images_from_soup
Description:    Download images from a BeautifulSoup object
Parameters:     soup (BeautifulSoup object), url (Optional string), return_images (Optional bool)
Returns:        images (List of BeautifulSoup tags) (optional)
'''
def download_images_from_soup(soup, url='', return_images=False):
    if (not re.search(r'^\s*$', url)):
        base_url, relative_url = get_base_and_relative(url)

    images = soup.find_all('img', src=True)

    for image in images:
        if (re.search(r'[^/]+\.((png)|(gif)|(jpe?g)|(jpe)|(jif)|(jfif?)|(svg)|(tiff?))', image['src'], re.IGNORECASE)):
            if ((not re.search(r'^https?://', image['src'])) and (not re.search(r'^www', image['src'])) and (not re.search(r'^file:///', image['src']))):
                if (not re.search(r'^\s*$', url)):
                    image['src'] = create_url_from_relative(image['src'], base_url, relative_url)
                else:
                    print('No URL was provided to find relative link: ' + image['src'])
                    continue

        download_image(image['src'])

    if (return_images == True):
        return images

'''
Function:       download_documents_from_soup
Description:    Download documents from a BeautifulSoup object
Parameters:     soup (BeautifulSoup object), url (Optional string)
'''
def download_documents_from_soup(soup, url=''):
    if (not re.search(r'^\s*$', url)):
        base_url, relative_url = get_base_and_relative(url)

    links = soup.find_all('a', href=True)
    documents = []

    for link in links:
        if (re.search(r'[^/]+\.((pdf)|(docx?)|(xlsx?)|(pptx?))', link['href'])):
            if ((not re.search(r'^https?://', link['href'])) and (not re.search(r'^www', link['href'])) and (not re.search(r'^file:///', link['href']))):
                if (not re.search(r'^\s*$', url)):
                    link['href'] = create_url_from_relative(link['href'], base_url, relative_url)
                else:
                    print('No URL was provided to find relative link: ' + link['href'])
                    continue

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
    download_images_from_soup(soup, url)

'''
Function:       download_documents_from_url
Description:    Download documents from a given URL
Parameters:     url (string)
'''
def download_documents_from_url(url):
    page_source = urllib.request.urlopen(url)
    page_source = page_source.read()
    soup = BeautifulSoup(page_source, 'html.parser')
    download_documents_from_soup(soup, url)
