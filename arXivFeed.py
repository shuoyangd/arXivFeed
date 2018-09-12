#! /usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib

import smtplib
from email.mime.text import MIMEText

from datetime import date

from arXivConfig import *

import os
import pdb

def feed2str(feed):
  # title = feed[0].split("Title:")[1]
  title = feed[0]
  authors = feed[1].split("Authors:")[1].split(",")
  authors = ", ".join(authors)
  link = feed[2]
  return title + '\n' + authors + '\n' + link

def send(emails, name, feeds):
  # write message
  msg_str = """Dear arXivFeed user:

With regard to your request for a daily feed of arXiv papers related to {0}, we are proud to present you the paper(s) that are uploaded since our last email.

""".format(name)

  for feed in feeds:
    msg_str += (feed2str(feed) + '\n\n')

  msg_str += """We hope you enjoy the feed today.

Regards,
arXivFeed

"""

  d = date.today()
  msg_str += d.strftime("%A, %B %d, %Y")

  # send message
  msg = MIMEText(msg_str, 'plain', 'utf-8')
  msg['Subject'] = "arXiv " + name + " feed " + d.strftime("%B %d, %Y")

  s = smtplib.SMTP('localhost')
  s.sendmail('localhost', emails, msg.as_string())
  s.quit()

if __name__ == "__main__":

  if os.path.exists(history_path):
    history = open(history_path).readlines()
  else:
    history = []

  for i in range(len(history)):
    history[i] = history[i].strip()

  for (feed_name, url) in urls:
    html = urllib.urlopen(url).read()
    parsed_html = BeautifulSoup(html)
    metas = parsed_html.body.findAll('li')
    titles = filter(lambda x: x is not None, \
        [meta.find('p', attrs={"class": "title is-5 mathjax"}) for meta in metas])
    stripped_titles = []
    for title in titles:
      items = filter(lambda x: x != u'', \
          [ item.text.strip() if hasattr(item, "text") else item.strip() for item in title ])
      stripped_titles.append(" ".join(items))
    titles = stripped_titles
    authors = filter(lambda x: x is not None, \
        [meta.find('p', attrs={"class": "authors"}) for meta in metas])
    authors = [author.text for author in authors]
    urls = filter(lambda x: hasattr(x, "a") and x.a is not None and (x.a.has_key("href")), \
        [ meta.find("span") for meta in metas ])
    urls = [url.a["href"] for url in urls]
    feeds = zip(titles, authors, urls)

    if feeds:
      send(emails, feed_name, feeds)

      history_file = open(history_path, 'w')
      for feed in feeds:
        history_file.write(str(feed[0]) + '\n')
      history_file.close()

