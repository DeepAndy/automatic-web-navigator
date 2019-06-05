import re
import urllib.request
from bs4 import BeautifulSoup
from date_converter import *

page_source = urllib.request.urlopen('https://www.ohio.edu/medicine/news-archive/')
soup = BeautifulSoup(page_source, 'html.parser')

for tag in soup.find_all('br'):
    tag.decompose()

f = open('url_and_date.txt', 'w')

for tag in soup.find_all('a', href=True):
    if (not (re.search(r'^https?://', tag['href']) and not re.search(r'^www', tag['href']) and not re.search(r'^file://', tag['href'])) or tag['href'].find('/') == 0):
        tag['href'] = 'https://www.ohio.edu/medicine/news-archive/' + tag['href']

    f.write(tag['href'] + '\n')
    print(tag['href'])
    found_date = False

    for text in tag.parent.contents:
        text = str(text)
        text = re.sub(r'[^a-zA-Z0-9 ]+', '', text)
        text = text.strip()

        if (re.search(r'\w+ \d+ \d+', text)):
            date = text
            date = re.search(r'(\w+ \d+ \d+)', text).group(1)
            found_date = True
            break

    if (found_date == True):
        date = date_converter(date)
    else:
        date = ''

    f.write(date + '\n')
    print(date)
