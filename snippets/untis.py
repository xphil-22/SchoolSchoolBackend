#API IMPORTS
import webuntis
import datetime
import json
import ast
import time

#SELENIUM IMPORTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from snippets import Ical
import os

class Untis:
    def __init__(self):
        self._session = 0
        
    def newSession(self, username, password):
        try:
            s = webuntis.Session(
                server='https://terpsichore.webuntis.com',
                username= username,
                password= password,  
                school='RFGS-Freiburg', 
                useragent='WebUntis Test'
            ).login()
            self._session = s
            
            return True

        except:
            return False
    
    def getClasses(self):
        return self._session.klassen()
    
    def getSubjects(self, className):
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        friday = monday + datetime.timedelta(days=6)
        print("monday ",monday)
        print("friday",friday)
        klasse = self._session.klassen().filter(name=className)[0]  
        tt = self._session.timetable(klasse=klasse, start=monday, end=friday)
        
        ID_List = []
        for subject in tt:       
            s = str(subject)
            ID_List.append(int(s[s.find('su')+13:s.find(']', s.find('su'))-1]))

        ID_List = list(set(ID_List)) #To clear the array from duplicates
            
        subject_list = [str(subject) for subject in self._session.subjects()
                        if subject.id in ID_List]
        
        
        return subject_list
    
    
    
    "SELENIUM STUFF STARTS HERE"
class WebsiteUntis:
    
    def __init__(self, username, password):
        self._ical = 0
        self._username = username
        self._password = password
        self._filePath = ""
        
        self._options = webdriver.ChromeOptions()
        self._options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self._options.add_argument("--no-sandbox")
        self._options.add_argument("--headless")
        self._options.add_argument("--disable-dev-sh-usage")
        prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory": 
                        os.getcwd() + "\Ical_Files", #Current Directory
             "directory_upgrade": True}
        self._options.add_experimental_option("prefs", prefs)
        
        
    def getWebSubjects(self):        
        self._setFilePath()
        self.downloadIcal()
        self._ical = Ical.Ical(self._filePath)
        return self._ical.getSubjectData()
        
    def _setFilePath(self):
        name = self._username.replace('ss','ß').split('.')
        fileName = name[1][0:6].capitalize() + name[0][0:3].capitalize()
        self._filePath = f"Ical_Files\{fileName}.ics"
        if os.path.exists(self._filePath):
            os.remove(self._filePath)
        
    
    def downloadIcal(self):
        #driver = webdriver.Chrome(chrome_options=self._options)
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=self._options)
        driver.set_window_position(0, 0)
        driver.set_window_size(1902, 768)
        
        driver.get("https://terpsichore.webuntis.com/WebUntis/?school=RFGS-Freiburg#/basic/login")
        input_fields = driver.find_elements(By.CLASS_NAME, 'un-input-group__input')
        input_fields[0].send_keys(self._username)
        input_fields[1].send_keys(self._password)
        driver.find_element(By.CLASS_NAME, 'redesigned-button').click()

        tt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/div/a[5]/div/div/div[2]')))
        tt.click()
        
        elements = driver.find_elements(By.TAG_NAME, 'button')
        for i in elements:
            print(str(i)+"\n")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'embedded-webuntis')))
        driver.switch_to.frame('embedded-webuntis')

       
        sel = '#dijit_layout__LayoutWidget_0 > section > div > div > div.un-flex-pane.un-flex-pane--fixed.un-timetable-page__header > div > form > div.float-right.btn-group > button:nth-child(1)'
        ical_Download_Button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
        
        ical_Download_Button.click()
        
        while os.path.exists(self._filePath) == False:
            time.sleep(0.001)
        
