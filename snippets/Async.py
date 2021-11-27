from my_globals import *

class Async:
    __AsyncData = []
    __AsyncProcesses = []
    
    def addData(self, item):
        Async.__AsyncData.append(item)
    
    def removeData(self, item):
        Async.__AsyncData.remove(item)
    
    def getData(self):
        return Async.__AsyncData
    
    
    def removeProcess(self, item):
        Async.__AsyncProcesses.remove(item)
    
    def addProcess(self, item):
        Async.__AsyncProcesses.append(item)
    
    def getProcesses(self):
        return Async.__AsyncProcesses