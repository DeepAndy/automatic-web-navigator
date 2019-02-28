f = open("scripps-article-ids.txt", "r")
lines = f.read()
url = "https://author.oit.ohio.edu/scrippscollege/newsevents/news-story.cfm?newsItem="
ids = lines.split(",,")

for num in range(len(ids)):
    ids[num] = url + ids[num]

f1 = open("web-queues/scripps_article_urls.wq", "w")
for id in ids:
    f1.write(id + "\n")
