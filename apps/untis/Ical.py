from django.core.files import File
import os

local = False

class Ical:
    
    def __init__(self, FilePath, FileName): #name.ics  #tmp\ #ical\
            
        self._filePaths = []
        self._IcalStrings = []
        
        if os.path.exists(f"{FilePath}first{FilePath[-1]}{FileName}"):
            self._filePaths.append(f"{FilePath}first{FilePath[-1]}{FileName}")
            
        if os.path.exists(f"{FilePath}sec{FilePath[-1]}{FileName}"):
            self._filePaths.append(f"{FilePath}sec{FilePath[-1]}{FileName}")
            
        if os.path.exists(f"{FilePath}third{FilePath[-1]}{FileName}"):
            self._filePaths.append(f"{FilePath}third{FilePath[-1]}{FileName}")
        
        for i in range(len(self._filePaths)):
            print(i)
            with open(self._filePaths[i], 'r') as f:
                myFile = File(f)
                self._IcalStrings.append(myFile.read())
        
           
    def getSpecificData(self, key):
        komma = self._IcalString.find(':' , self._IcalString.find(key))+1
        return self._IcalString[komma: self._IcalString.find('\n', komma)]

    def getSubjectData(self):
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