from messageStore import MessageStore

class MessageStoreArray():

    #Initializes a list of MessageStore Objects
    def __init__(self, defaulStr = "", defaultLitState = False, numCandles = 20, specialLanternNum = 2):
        self._msgStoreArr = []
        specialMsgFile = open('specialMsg.txt',mode='r')
        specialMsgStr =""
        for line in specialMsgFile.readlines():
            specialMsgStr+= line
        
        specialMsgFile.close()

        for i in range(numCandles):
            if i==specialLanternNum:
                self._msgStoreArr.append(MessageStore(tempstr=specialMsgStr,lit=True, isSpecialLantern=True))
                continue
            self._msgStoreArr.append(MessageStore(tempstr= defaulStr ,lit= defaultLitState, isSpecialLantern=False))

    
    def getMsgStoreList(self):
        return self._msgStoreArr
    
    def resetAllMsgStores(self):
        for candle in self._msgStoreArr:
            if not candle.isSpecialLantern():
                candle.setMsg("")
                candle.setLit(False)
    
    def resetMsgStoreAtIndex(self, index):
        self._msgStoreArr[index].setLit(False)
        self._msgStoreArr[index].setMsg("")



        

