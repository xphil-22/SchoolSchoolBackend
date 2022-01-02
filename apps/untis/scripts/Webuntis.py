import os
from untis.scripts.Thread import Thread 
from untis.scripts.UntisAPI import UntisAPI
from untis.scripts.Ical import Ical
local = False #To set the differences between Local Variables and Server Variables

class WebsiteUntis:
    
    Data = []       #Static Attribut to store the Requested Data
    Threads = []    #Static Attribut to store the current working Threads
    
    def __init__(self, profile) -> None:
        self._ical = 0
        self._profile = profile
        self._username = profile.untisUsername
        self._filePath = ""
        self._scrapingWaitTime = 30
        self._fileName = ""
        
    def Login(self) -> bool:
        untis = UntisAPI()
        return untis.newSession(self._profile.untisUsername, self._profile.untisPassword)
    
    def getWebSubjects(self) -> dict:
        if self._username not in WebsiteUntis.Threads and not self.proofData():
            self._setFilePath()            
            t = Thread(owner=self._username, target=self._getIcals, args=(WebsiteUntis.Data, WebsiteUntis.Threads))
            WebsiteUntis.Threads.append(t.getOwner()) 
            t.start()
            return {"done": 2}
    
        if self._username in WebsiteUntis.Threads and not self.proofData():
            return {"done": 1}
        
        if self.proofData():
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
        if Ical.local:
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
            print("Trueeeeeeeeeeee")
            Data.append({self._username : data})
            print(data)
            Processes.remove(self._username)       
            
        except Exception as e: 
            print(e)
            Processes.remove(self._username)
