from django.core.files import File
import os
class Ical:
    
    def __init__(self, FilePath):
        print(FilePath)
        self._filePaths = []
        self._IcalStrings = []
        
        if os.path.exists(FilePath):
            self._filePaths.append(FilePath)
            
        if os.path.exists(f"{FilePath[:-4]} (1).ics"):
            self._filePaths.append(f"{FilePath[:-4]} (1).ics")
            
        if os.path.exists(f"{FilePath[:-4]} (2).ics"):
            self._filePaths.append(f"{FilePath[:-4]} (2).ics")
        
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
    
if __name__ == '__main__':
    i = Ical("Ical_Files\KuhlmaMay.ics")
    print(i.getSubjectData())