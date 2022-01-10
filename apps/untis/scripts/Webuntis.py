import os
from untis.scripts.Thread import Thread 
from untis.scripts.UntisAPI import UntisAPI
from untis.scripts.Ical import Ical
from SchoolSchoolBackend.settings import LOCAL as local

class WebsiteUntis:
    
    Data:list = []       #Static Attribut to store the Requested Data
    Threads:list[Thread] = []    #Static Attribut to store the current working Threads
    
    def __init__(self, profile:list[str]) -> None:
        self._ical:Ical = 0
        self._profile:list[str] = profile
        self._username:str = profile.untisUsername
        self._filePath:str = ""
        self._scrapingWaitTime:int = 30
        self._fileName:str = ""
        
    def Login(self) -> bool: #check given credentials are wrong or right
        untis = UntisAPI()
        return untis.newSession(self._profile.untisUsername, self._profile.untisPassword)
    
    def getWebSubjects(self) -> dict: #return subjects of icals 
        if self._username not in WebsiteUntis.Threads and not self.proofData():
            self._setFilePath()            
            t = Thread(owner=self._username, target=self._getIcals, args=(WebsiteUntis.Data, WebsiteUntis.Threads)) #start new thread to download icals
            WebsiteUntis.Threads.append(t.getOwner()) 
            t.start()
            return {"done": 2} #main thread return done:2 while the other thread downloads the icals
    
        if self._username in WebsiteUntis.Threads and not self.proofData(): #if thread is started but the downloads aren't finished yet, the server return done:1
            return {"done": 1}
        
        if self.proofData(): #If ical download is completed the server returns them
            data = [el[self._username] for el in WebsiteUntis.Data if self._username in el]
            WebsiteUntis.Data = [el for el in WebsiteUntis.Data if self._username not in el]
            return {"done":0, "Subjects":data[0]}

        else:
            return {"done": -1}
        
    def proofData(self) -> bool:
        for el in WebsiteUntis.Data:
            if self._username in el:
                return True
        return False
        
    def _setFilePath(self) -> None:
        name = self._username.replace('ss','ß').split('.')
        self._fileName = name[1][0:6].capitalize() + name[0][0:3].capitalize() + ".ics"
        self._filePath = "tmp/" 
        c = '/'
        print("local: ", local)
        if local:
            c = '\\'
            self._filePath = "apps\\untis\\Ical_Files\\"
            
        print(f"{self._filePath}NextWeek{c}{self._fileName}")
        if os.path.exists(f"{self._filePath}NextWeek{c}{self._fileName}"):
            os.remove(f"{self._filePath}NextWeek{c}{self._fileName}")
        
        if os.path.exists(f"{self._filePath}ThisWeek{c}{self._fileName}"):
            os.remove(f"{self._filePath}ThisWeek{c}{self._fileName}")
            
        if os.path.exists(f"{self._filePath}LastWeek{c}{self._fileName}"):
            os.remove(f"{self._filePath}LastWeek{c}{self._fileName}")
    
        
    def _getIcals(self, Data, Processes) -> None:
        try:
            ical = Ical(self._filePath, self._fileName, self._profile)
            data = ical.getIcals()
            if data == []:
                self._setFilePath()
                self._getIcals(Data, Processes)
                
            print("Trueeeeeeeeeeee")
            Data.append({self._username : data})
            print(data)
            Processes.remove(self._username)       
            
        except Exception as e: 
            print(e)
            Processes.remove(self._username)
