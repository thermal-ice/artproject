

class MessageStore():

    def __init__(self,tempstr, lit, isSpecialLantern):
        self._singleMsg =tempstr
        self._isLit = lit
        self._isSpecialLantern = isSpecialLantern

    def getMsg(self):
        return self._singleMsg

    def setMsg(self,newMsg):
       self._singleMsg = newMsg
    
    def getIsLit(self):
        return self._isLit
    
    def setLit(self, newLitVal):
        self._isLit = newLitVal
    
    def isSpecialLantern(self):
        return self._isSpecialLantern
    



    

