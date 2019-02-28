'''
Author:         Austin Moore
Script Type:    Main Script
Description:    Quick script to create a web queue from a list of URL IDs given
                to me
Python 3.7.2
'''

import re

f = open("scrippsids.txt", "r")
ids = f.readlines()
url = "https://author.oit.ohio.edu/scrippscollege/newsevents/news-story.cfm?newsItem="
index2 = 0

for index in ids:
    full_url = url + index
    ids[index2] = full_url
    index2 += 1

print(ids)
f.close()
f = open("web-queues/scrippsurls.wq", "w")

for index in ids:
    f.write(index)
