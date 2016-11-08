from BeautifulSoup import BeautifulSoup
import urllib

import smtplib
from email.mime.text import MIMEText

from datetime import date

from arXivConfig import *

def feed2str(feed):
  title = feed[0].split("Title:")[1]
  authors = feed[1].split("Authors:")[1].split(",")
  authors = ", ".join(authors)
  link = feed[2]
  return title + '\n' + authors + '\n' + link

def send(emails, name, feeds):
  # write message
  msg_str = """Dear arXivFeed user:

  With regard to your request for a daily feed of arXiv papers related to {0}, we are pround to present you the paper(s) that are uploaded since our last email.

""".format(name)
  
  for feed in feeds:
    msg_str += (feed2str(feed) + '\n\n')

  msg_str += """We hope you enjoy the feed presented today.

Regards,
arXivFeed
"""

  d = date.today()
  msg_str += d.strftime("%A, %B %d, %Y")

  # send message
  msg = MIMEText(msg_str)
  msg['Subject'] = "arXiv " + name + " feed " + d.strftime("%B %d, %Y")

  s = smtplib.SMTP('localhost')
  s.sendmail('localhost', emails, msg.as_string())
  s.quit()

if __name__ == "__main__":
  
  history = []
  # history = open(history_path).readlines()
  for i in range(len(history)):
    history[i] = history[i].strip()

  for (feed_name, url) in urls:
    html = urllib.urlopen(url).read()
    parsed_html = BeautifulSoup(html)
    metas = parsed_html.body.findAll('dd')
    links = parsed_html.body.findAll('dt')
    feeds = []
    for (meta, link) in zip(metas, links):
      title = meta.find("div", attrs = {'class': "list-title mathjax"}).text
      if title in history:
        break
  
      authors = meta.find("div", attrs = {'class': "list-authors"}).text
      pdfurl = "https://arxiv.org" + link.find("a", attrs = {'title': "Download PDF"}).get("href")
      feeds.append((title, authors, pdfurl))
  
    if feeds:
      for email in emails:
        send(email, feed_name, feeds)

