import urllib.request
import re

'''
Function:       download_image
Description:    Download an image from a string link
Parameters:     image (string)
'''
def download_image(image):
    try:
        file_name = re.search(r'\..*/(.*\..*)', image).group(1)
    except:
        pass

    try:
        urllib.request.urlretrieve(image, "images/" + file_name)
        print('Successfully downloaded ' + file_name)
    except Exception as e:
        print("Failed to download image at \"" + image + "\"")
        print(e)

        return

'''
Function:       download_document
Description:    Download a document from a string link
Parameters:     document (string)
'''
def download_document(document):
    try:
        file_name = re.search(r'\..*/(.*\..*)', document).group(1)
    except:
        pass

    try:
        urllib.request.urlretrieve(document, "documents/" + file_name)
        print('Successfully downloaded ' + file_name)
    except Exception as e:
        print("Failed to download image at \"" + document + "\"")
        print(e)

        return

'''
Function:       download_images_from_soup
Description:    Download images from a BeautifulSoup object
Parameters:     soup (BeautifulSoup object)
'''
def download_images_from_soup(soup):
    images = soup.find_all('img', src=True)

    for image in images:
        if (image['src'].find('/') == 0):
            image['src'] = 'https://www.ohio.edu' + image['src']

        download_image(image['src'])

'''
Function:       download_images_from_soup_return
Description:    Download images from a BeautifulSoup object and return a list
                of images as BeautifulSoup objects
Parameters:     soup (BeautifulSoup object)
Returns:        images (BeautifulSoup object)
'''
def download_images_from_soup_return(soup):
    images = soup.find_all('img', src=True)

    for image in images:
        if (image['src'].find('/') == 0):
            image['src'] = 'https://www.ohio.edu' + image['src']

        download_image(image['src'])

    return images


'''
Function:       download_documents_from_soup
Description:    Download documents from a BeautifulSoup object
Parameters:     soup (BeautifulSoup object)
'''
def download_documents_from_soup(soup):
    links = soup.find_all('a', href=True)
    documents = []

    for link in links:
        if (re.search('r(\.docx?)|(\.pptx?)|(\.xlsx?)|(\.pdf)|(\.zip)', link['href'])):
            if (link['href'].find('/') == 0):
                link['href'] = 'https://www.ohio.edu' + link['href']

            documents.append(link['href'])

    for document in documents:
        download_document(document)
