import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
import os
from datetime import *
from dateutil.relativedelta import *
import time

class Leet:
  def __init__(self):
    cache_dir = os.path.expanduser("~/.cache/leet")
    if not os.path.exists(cache_dir):
      os.mkdir(cache_dir)
    self.cache_file = os.path.join(cache_dir, "data.json")
    if os.path.exists(self.cache_file):
      with open(self.cache_file, "r") as f:
        self.items = json.load(f)
    else:
      self.items = json.loads("[]")
  
  def get_json(self):
    self.items = json.loads("[]")
    root = "https://1337x.to"
    base = root+"/johncena141-torrents/"
    first = base+"1/"
    r = requests.get(first)
    soup = BeautifulSoup(r.text, 'html.parser')
    last = int(soup.find("li", {"class": "last"}).a["href"].split("/")[-2])
    def get_page(soup):
      for el in soup.find_all("td", {"class": "coll-1 name"}):
        for a in el.find_all("a"):
          if a["href"].startswith("/torrent"):
            time_str = a.parent.parent.find("td", {"class": "coll-5"}).text.split(" ")
            # add 's' to the end if it doesn't have it
            if time_str[1][-1] != "s":
              time_str[1] += "s"
            try:
              date = datetime.now()+relativedelta(**{time_str[1]: int('-'+time_str[0])})
            except:
              date = datetime.min

            units = {"B": 1, "KB": 10**3, "MB": 10**6, "GB": 10**9, "TB": 10**12}
            size = a.parent.parent.find("td", {"class": "size"}).text.split(" ")
            size = int(float(size[0])*units[size[1][0:2]])

            self.items.append({"name":a.text, "url": root + a["href"], "date":date.strftime("%Y-%m-%d"), "size":size})
    def get_pages(url):
      r = requests.get(url)
      soup = BeautifulSoup(r.text, 'html.parser')
      get_page(soup)
    get_page(soup)
    with ThreadPoolExecutor(max_workers=10) as executor:
      executor.map(get_pages, [base + str(x) + "/" for x in range(2, last+1)])
    with open(self.cache_file, "w") as f:
      json.dump(self.items, f)
    return self.items
