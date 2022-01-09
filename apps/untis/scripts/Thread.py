import threading

#Thread class to start a new thread associated with a user
class Thread:

    def __init__(self, *args:list,  **kwargs:list):

        if len(kwargs) > 2: 
            self._owner:str = kwargs['owner']
            self._target:function = kwargs['target']
            self._args:list = kwargs['args']
            self._t:threading.Thread = threading.Thread(target=self._target, args=self._args)
            
        elif len(kwargs) == 1:
            self._target:function = kwargs['target']
            self._t:threading.Thread = threading.Thread(target=self._target)
    
    def waitUntilCompleted(self):
        self._t.join()
        
    def start(self):
        self._t.start()
    
    def getOwner(self):
        return self._owner