from django.core.files import File

class Ical:
   
    def __init__(self, FilePath):
        self._IcalString = ""
        with open(FilePath, 'r') as f:
            myFile = File(f)
            
            self._IcalString = myFile.read()
           
    def getSpecificData(self, key):
        komma = self._IcalString.find(':' , self._IcalString.find(key))+1
        return self._IcalString[komma: self._IcalString.find('\n', komma)]

    def getSubjectData(self):
        SubjectData = []
        arr = self._IcalString.split('\n')
        for i in range(len(arr)):
            if "LOCATION" in arr[i]:
                a = arr[i][arr[i].find(':')+1:]
                b = a.split(' ')
                c = b[-2]
                element = [arr[i+1][arr[i+1].find(':')+1:] , c] 
                if element not in SubjectData:
                    SubjectData.append(element)               
        return SubjectData
    