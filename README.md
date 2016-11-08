# arXivFeed

---

This is a small tool that crawls an [arXiv](https://arxiv.org/) search result page and send a email containing new papers if there is any.

#### Dependencies

+ BeautifulSoup >= 3.2.1

#### Installation

You only need to update the configurations in `arXivConfig.py` into yours to be able to receive email. To make this script automatically run everyday, I personally use crontab. My crontab line is:

```
0 18 * * * /home/shuoyangd/arXivFeed/arXivFeed.py
```

which means the script will be executed everyday at 18:00.

