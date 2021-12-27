import requests
from lxml import etree
from bs4 import BeautifulSoup

class WebsiteGraber:
    def __init__(self, url:str) -> None:
        self._url = url
        self._html = None
        
    def downloadWebsite(self):
        site = requests.get(self._url)
        self.formatHtml(site)
        
    def formatHtml(self, site):
        soup = BeautifulSoup(site.text, features="lxml")
        self._html = etree.HTML(str(soup))
    
    def getWebsite(self):
        return self._html