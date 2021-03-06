from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from untis.scripts.Thread import Thread
from SchoolSchoolBackend.settings import LOCAL as local
import os
import time
class Selenium:
    
    def __init__(self, ver:str, profile:list[str], fileName:str, filePath:str):
        self._filePath:str = filePath
        self._fileName:str = fileName
        self._profile:list[str] = profile
        self._driver:webdriver = None
        self._args:list[str] = ["--log-level=3", "--no-sandbox", "--disable-dev-sh-usage", "--headless"] 
        self._v:str = ver
        self._selector:str = '#dijit_layout__LayoutWidget_0 > section > div > div > div.un-flex-pane.un-flex-pane--fixed.un-timetable-page__header > div > form > div.float-right.btn-group > button:nth-child(1)'
        
    def _getChromeOptions(self):
        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        
        for arg in self._args:
            options.add_argument(arg)
        
        path =  f"tmp/{self._v}/" #Current Directory
        if local:
            path =   f"{os.getcwd()}\\apps\\untis\\Ical_Files\\{self._v}" #Current Server Directory
        print("download Path: ", path)
        prefs = {"profile.default_content_settings.popups": 0,
            "download.default_directory": path,
            "directory_upgrade": True}
        
        options.add_experimental_option("prefs", prefs)
        return options
    
    def start(self) -> None:
        if not local:
            self._driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=self._getChromeOptions())
        else:
            self._driver = webdriver.Chrome(chrome_options=self._getChromeOptions())
        self._driver.set_window_position(0, 0)
        self._driver.set_window_size(1902, 768)
    
        self._driver.get("https://terpsichore.webuntis.com/WebUntis/?school=RFGS-Freiburg#/basic/login")
        WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'un-input-group__input')))
        input_fields = self._driver.find_elements(By.CLASS_NAME, 'un-input-group__input')
        input_fields[0].send_keys(self._profile.untisUsername)
        input_fields[1].send_keys(self._profile.untisPassword)
        self._driver.find_element(By.CLASS_NAME, 'redesigned-button').click()
        tt = WebDriverWait(self._driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/div/a[5]/div/div/div[2]')))
        tt.click()
        self._driver.refresh()
        WebDriverWait(self._driver, 30).until(EC.presence_of_element_located((By.ID, 'embedded-webuntis')))
        self._driver.switch_to.frame('embedded-webuntis')
    
    def stopSelenium(self) -> None:
        self._driver.quit()
        
        
    def downloadThisWeek(self) -> None:
        try:
            self.start()
            WebDriverWait(self._driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, self._selector))).click()
        
            while self.proofDownloadCompleted():
                time.sleep(0.001)
            self.stopSelenium()
        except Exception as e:
            print("downalodThisWeekException: ", e)
    
    def downloadNextWeek(self) -> None:
        try:
            self.start()
            pageButtonForward = '#dijit_layout__LayoutWidget_0 > section > div > div > div.un-flex-pane.un-flex-pane--fixed.un-timetable-page__header > div > form > div.un-date-selector.form-group > span > span:nth-child(3) > button'
            WebDriverWait(self._driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, pageButtonForward))).click()
            time.sleep(0.5)
            WebDriverWait(self._driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, self._selector))).click()
        
            while self.proofDownloadCompleted():
                time.sleep(0.001)
                
            self.stopSelenium()
            
        except Exception as e:
            print("downloadIcalNextWeek exception: ", e)
           
            
    def downloadLastWeek(self) -> None:
        try:
            self.start()
            pageButtonBack = '#dijit_layout__LayoutWidget_0 > section > div > div > div.un-flex-pane.un-flex-pane--fixed.un-timetable-page__header > div > form > div.un-date-selector.form-group > span > span:nth-child(1) > button > i'
            WebDriverWait(self._driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, pageButtonBack))).click()
            time.sleep(0.5)
            WebDriverWait(self._driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, self._selector))).click()
            while self.proofDownloadCompleted():
                time.sleep(0.001)
            self.stopSelenium()
        except Exception as e:
            print("downloadIcalLastWeek exception: ", e)
        
    def proofDownloadCompleted(self) -> bool:
        c = '/'
        if local:
            c = '\\'
        print(f"{self._filePath}{self._v}{c}{self._fileName}")
        if os.path.exists(f"{self._filePath}{self._v}{c}{self._fileName}"):
            return False
        return True
        
