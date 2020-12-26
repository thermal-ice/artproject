
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


class GSheets():

    # Fields
    specialMsgRange = "B2:B20"

    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds",
                 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",
                                                                 scope)

        client = gspread.authorize(creds)

        self.spreadSheet = client.open("artproject_database")
        self.firstSheet = self.spreadSheet.sheet1
        self.secondSheet = self.spreadSheet.get_worksheet(1)
        self.thirdSheet = self.spreadSheet.get_worksheet(2)
        self.fourthSheet = self.spreadSheet.get_worksheet(3)

    # Helper functions


    def checkMsgExists(self, index):
        existsVal = self.firstSheet.acell("B" + str(index)).value
        if existsVal == "SM" or existsVal == "1":
            return True
        # existVal must be '0' then
        return False

    def concatMultipleStrsWithNewline(self,strArr):
        return ''.join([(paragraph[0]+'\n') for paragraph in strArr])


    def getCurrMessagesRowRange(self, rowNum):
        # Currently set to be the 'B' and 'C' cols
        return 'B' + str(rowNum) + ':' + 'C' + str(rowNum)

    def getSpecialMsg(self,indices= specialMsgRange):
        msgArr = self.fourthSheet.get(indices)

        return self.concatMultipleStrsWithNewline(strArr= msgArr)




    # Second column is MsgExist col, values start from index 1
    def getMsgExistsList(self):
        return self.firstSheet.col_values(2)[1:]




    def newMsgChange(self,candleNum, newMsg):
        updatesArr = []

        index = candleNum + 1

        prevNumOfChanges = int(self.secondSheet.cell(col=2, row=index).value)

        changeIndex = prevNumOfChanges + 3


        changeCellRecordAddress = self.secondSheet.cell(row=index,col=changeIndex).address

        updatesArr.append({'range': 'B' + str(index), 'values':
            [[prevNumOfChanges + 1]]})

        updatesArr.append({'range': changeCellRecordAddress, 'values': [[newMsg]]})

        self.secondSheet.batch_update(updatesArr)








    def addMsg(self, message, candleNum):
        currIndex = candleNum + 1  # Offset of 1 for the table

        if self.checkMsgExists(index=currIndex):
            return False  # Message already exists

        rowRange = self.getCurrMessagesRowRange(currIndex)

        # Message doesn't exist yet, adding it now
        self.firstSheet.update(rowRange, [[1, message]])

        # Adding newest message to the MsgChanges table

        self.newMsgChange(candleNum=candleNum,newMsg=message)

        return True


    def getMessage(self, candleNum):
        return self.firstSheet.cell(col=3, row=candleNum+1).value

    def resetSingleMessage(self,candleNum):
        rowRange = self.getCurrMessagesRowRange(rowNum=candleNum+1)
        self.firstSheet.update(rowRange, [[0, ""]])  # Setting it to empty string again

        now = datetime.now()
        self.thirdSheet.append_row([candleNum,now.strftime("%m/%d/%Y"), now.strftime("%H:%M:%S")])

    def resetAllMessages(self):
        msgExistList = self.getMsgExistsList()

        updatesArr = []
        for i in range(len(msgExistList)):
            if msgExistList[i] == "1":
                updatesArr.append({'range': self.getCurrMessagesRowRange(i+2), 'values':[[0,""]]})

        self.firstSheet.batch_update(updatesArr)

        now = datetime.now()
        self.thirdSheet.append_row(
            ["All", now.strftime("%m/%d/%Y"), now.strftime("%H:%M:%S")])