import requests
from bs4 import BeautifulSoup
from requests.models import parse_url
from urllib.parse import urlparse

class Game:
  def __init__(self, url):
    self.url = url
    self.parse_info(self.url)

  def soup_magnet(self, href: str):
    return href.startswith('magnet:')
  
  def parse_info(self, url):
    url += '/' if not url.endswith('/') else ''
    r = requests.get(url)
    if r.status_code != 200:
      raise Exception('Invalid url')
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
      self.magnet = soup.find("a", href=self.soup_magnet)['href']
    except:
      self.magnet = ""
    """
    container = soup.find('div', {'id': 'description'})
    try:
      self.poster = container.find('img')['data-original']
    except:
      self.poster = ""
    try:
      self.title = container.find("span", {"style": "font-size: 34px"}).text
    except:
      self.title = ""
    try:
      self.sub_title = container.find("span", {"style": "font-size: 24px"}).text
    except:
      self.sub_title = ""
    try:
      self.desc = container.text
    except:
      self.desc = ""
    """
