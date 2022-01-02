import threading

class Thread:

    def __init__(self, *args,  **kwargs):
        print(len(kwargs))
        if len(kwargs) > 2: 
            self._owner = kwargs['owner']
            self._target = kwargs['target']
            self._args = kwargs['args']
            self._t = threading.Thread(target=self._target, args=self._args)
            
        elif len(kwargs) == 1:
            self._target = kwargs['target']
            self._t = threading.Thread(target=self._target)
    
    def waitUntilCompleted(self):
        self._t.join()
        
    def start(self):
        self._t.start()
    
    def getOwner(self):
        return self._owner