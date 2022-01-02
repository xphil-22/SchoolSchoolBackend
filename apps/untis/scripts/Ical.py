from django.core.files import File
from untis.scripts.Selenium import Selenium
from untis.scripts.Thread import Thread
import os



class Ical:
    
    local = False
    
    def __init__(self, filePath, fileName, profile):
        self._filePath = filePath
        self._fileName = fileName
        self._Profile = profile
        self._icals = ['ThisWeek', 'LastWeek','NextWeek']
        
        self._filePaths = []
        self._IcalStrings = []
        
           
    def getSpecificData(self, key):
        komma = self._IcalString.find(':' , self._IcalString.find(key))+1
        return self._IcalString[komma: self._IcalString.find('\n', komma)]

    def _getSubjectData(self):
        SubjectData = []
        for i in range(len(self._filePaths)):
            arr = self._IcalStrings[i].split('\n')
            for i in range(len(arr)):
                if "LOCATION" in arr[i]:
                    a = arr[i][arr[i].find(':')+1:]
                    b = a.split(' ')
                    c = b[-2]
                    element = [arr[i+1][arr[i+1].find(':')+1:] , c] 
                    if element not in SubjectData:
                        SubjectData.append(element)     
        return SubjectData
    
    def getIcals(self):
        sel = []
        for ical in self._icals:
            sel.append(Selenium(ical, self._Profile, self._fileName, self._filePath))
            
        funcs = [sel[0].downloadThisWeek, sel[1].downloadLastWeek, sel[2].downloadNextWeek]
        threads = []
        
        for func in funcs:
            print("xxxxxxx")
            t = Thread(target=func)
            print("yyyy")
            t.start()
            print('zzzz')
            threads.append(t)
        
        for th in threads:
            th.waitUntilCompleted()
        
        self._readIcals()
        data = self._getSubjectData()
        return data     

            
    def _readIcals(self):
        if os.path.exists(f"{self._filePath}NextWeek{self._filePath[-1]}{self._fileName}"):
                self._filePaths.append(f"{self._filePath}NextWeek{self._filePath[-1]}{self._fileName}")
            
        if os.path.exists(f"{self._filePath}LastWeek{self._filePath[-1]}{self._fileName}"):
            self._filePaths.append(f"{self._filePath}LastWeek{self._filePath[-1]}{self._fileName}")
            
        if os.path.exists(f"{self._filePath}ThisWeek{self._filePath[-1]}{self._fileName}"):
            self._filePaths.append(f"{self._filePath}ThisWeek{self._filePath[-1]}{self._fileName}")
        
        for i in range(len(self._filePaths)):
            print(i)
            with open(self._filePaths[i], 'r') as f:
                myFile = File(f)
                self._IcalStrings.append(myFile.read())