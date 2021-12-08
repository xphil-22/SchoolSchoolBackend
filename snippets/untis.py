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

from threading import Thread
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


local = False   
class WebsiteUntis:
    
    Data = []
    Threads = []
    ThreadTime = []
    
    def __init__(self, username, password):
        self._ical = 0
        self._username = username
        self._password = password
        self._userData = f"{self._username}"
        self._filePath = ""
        self._ScrapingWaitTime = 30
        self._fileName = ""

    
    def getWebSubjects(self):
        print(WebsiteUntis.Threads, WebsiteUntis.Data)
        
        if self._userData not in WebsiteUntis.Threads and not self.proofData():
            self._setFilePath()
            WebsiteUntis.Threads.append(self._userData)
            WebsiteUntis.ThreadTime.append({self._userData : time.time()})
            t = Thread(target=self.getIcals, args=(WebsiteUntis.Data, WebsiteUntis.Threads))
            t.start()
            return {"done": 2}
        
        if self._userData in WebsiteUntis.Threads and not self.proofData():
            return {"done": 1}
        
        if self.proofData():
            data = [el[self._userData] for el in WebsiteUntis.Data if self._userData in el]
            WebsiteUntis.Data = [el for el in WebsiteUntis.Data if self._userData not in el]
            WebsiteUntis.ThreadTime = [el for el in WebsiteUntis.ThreadTime if self._userData not in el]
            
            return {"done":0, "Subjects":data[0]}

        else:
            return {"done": -1}
                
    def proofData(self):
        for el in WebsiteUntis.Data:
            if self._userData in el:
                return True
        return False
    
    def proofThreadTime(self):
        now = time.time()
        for el in WebsiteUntis.ThreadTime:
            for ThreadName in el:
                StartTime = el[ThreadName]
                print(now - StartTime)
                if now - StartTime > self._ScrapingWaitTime:
                    WebsiteUntis.Threads.remove(self._userData)
                    WebsiteUntis.ThreadTime = [el for el in WebsiteUntis.ThreadTime if self._userData not in el]
    
    def _setFilePath(self):
        name = self._username.replace('ss','ß').split('.')
        self._fileName = name[1][0:6].capitalize() + name[0][0:3].capitalize() + ".ics"
        self._filePath = f"tmp/" #<<
        c = '/'
        if local:
            c = '\\'
            self._filePath = "Ical_Files\\"
            
        if os.path.exists(f"{self._filePath}first{c}{self._fileName}"):
            os.remove(f"{self._filePath}first{c}{self._fileName}")
        
        if os.path.exists(f"{self._filePath}sec{c}{self._fileName}"):
            os.remove(f"{self._filePath}sec{c}{self._fileName}")
            
        if os.path.exists(f"{self._filePath}third{c}{self._fileName}"):
            os.remove(f"{self._filePath}third{c}{self._fileName}")
    

    def _getChromeOptions(self, v):
        print("options startet")
        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument("--log-level=3")
        options.add_argument("--no-sandbox")
        if not local:
            options.add_argument("--headless")
        else:
            options.add_argument("--headless")         
               
        options.add_argument("--disable-dev-sh-usage")
        print("opt 1")
        path =  f"tmp/{v}/" #Current Directory   #<<<
        if local:
            path =   f"{os.getcwd()}\Ical_Files\{v}" #Current Directory
        
        print("opt 2")
        prefs = {"profile.default_content_settings.popups": 0,
            "download.default_directory": path,
            "directory_upgrade": True}
        options.add_experimental_option("prefs", prefs)
        print("opt 3")
        return options
    
    def startSelenium(self, v):
        print("sel start")
        options = self._getChromeOptions(v)
        print("sel 1")
        
        print("sel 2")
        
        if not local:
            print("chrome options:", str(options))
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
        if local:
            driver = webdriver.Chrome(chrome_options=options)
               
        print("sel 3")
        print("Browser startet..")
        driver.set_window_position(0, 0)
        driver.set_window_size(1902, 768)
        
        driver.get("https://terpsichore.webuntis.com/WebUntis/?school=RFGS-Freiburg#/basic/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'un-input-group__input')))
        input_fields = driver.find_elements(By.CLASS_NAME, 'un-input-group__input')
        input_fields[0].send_keys(self._username)
        input_fields[1].send_keys(self._password)
        driver.find_element(By.CLASS_NAME, 'redesigned-button').click()
        tt = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/div/a[5]/div/div/div[2]')))
        tt.click()
        driver.refresh()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'embedded-webuntis')))
        driver.switch_to.frame('embedded-webuntis')
        print("sel 4")
        return driver
        
    def stopSelenium(self, driver):
        driver.quit()
    
    def proofDownloadCompleted(self, v):
        c = '/'
        if local:
            c = '\\'
        
        if os.path.exists(f"{self._filePath}{v}{c}{self._fileName}"):
            return False
        return True
            
    def getIcals(self, Data, Processes):
        try:
            print("2")
            funcs = [self.downloadIcalLastWeek,self.downloadIcalNextWeek] 
            threads = []
            print("3")
            for func in funcs:
                t = Thread(target=func)
                t.start()
                threads.append(t)
            
            for th in threads:
                th.join()
            
            print("Downloads beendet")
                
            self._ical = Ical.Ical(self._filePath, self._fileName)
            data = self._ical.getSubjectData()
            Data.append({self._userData : data})
            Processes.remove(self._userData)            
            print("4")
            
        except Exception as e: 
            print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeexxxxxxxxxxxxxxxxxxxxeeeeeeeeeeeeeeeeeeeeeptiooooooon")
            print(e)
            Processes.remove(self._userData)
            print("6")

    def downloadIcalThisWeek(self):
        print("download First Startet")
        driver = self.startSelenium("first")
        print("first 1")
        sel = '#dijit_layout__LayoutWidget_0 > section > div > div > div.un-flex-pane.un-flex-pane--fixed.un-timetable-page__header > div > form > div.float-right.btn-group > button:nth-child(1)'
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel))).click()
      
        while self.proofDownloadCompleted("first"):
            time.sleep(0.001)
        driver.quit()
        print("downloaded First Ical")
        
    def downloadIcalLastWeek(self):
        print("sec startet")
        driver = self.startSelenium("sec")
        print("sec 2")
        sel = '#dijit_layout__LayoutWidget_0 > section > div > div > div.un-flex-pane.un-flex-pane--fixed.un-timetable-page__header > div > form > div.float-right.btn-group > button:nth-child(1)'
        pageButtonBack = '#dijit_layout__LayoutWidget_0 > section > div > div > div.un-flex-pane.un-flex-pane--fixed.un-timetable-page__header > div > form > div.un-date-selector.form-group > span > span:nth-child(1) > button > i'
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, pageButtonBack))).click()
        time.sleep(0.5)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel))).click()
    
        while self.proofDownloadCompleted("sec"):
            time.sleep(0.001)
        driver.quit()
        print("downloaded Second Ical")
    
    def downloadIcalNextWeek(self):
        driver = self.startSelenium("third")
        sel = '#dijit_layout__LayoutWidget_0 > section > div > div > div.un-flex-pane.un-flex-pane--fixed.un-timetable-page__header > div > form > div.float-right.btn-group > button:nth-child(1)'
        pageButtonForward = '#dijit_layout__LayoutWidget_0 > section > div > div > div.un-flex-pane.un-flex-pane--fixed.un-timetable-page__header > div > form > div.un-date-selector.form-group > span > span:nth-child(3) > button'
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, pageButtonForward))).click()
        time.sleep(0.5)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel))).click()
      
        while self.proofDownloadCompleted("third"):
            time.sleep(0.001)
        driver.quit()
        print("downloaded Third Ical")
