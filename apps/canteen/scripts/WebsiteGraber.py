import requests
from lxml import etree
from bs4 import BeautifulSoup

class WebsiteGraber:
    def __init__(self, url:str) -> None:    
        self._url:str = url
        self._html:str = None
        
    def downloadWebsite(self):
        site = requests.get(self._url) #download HTML Code using requests module
        self.formatHtml(site) #format HTML into etree HTML object
        
    def formatHtml(self, site:str):
        soup = BeautifulSoup(site.text, features="lxml")
        self._html = etree.HTML(str(soup))
    
    def getWebsite(self): #return html object
        return self._html