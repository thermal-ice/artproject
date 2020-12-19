from main import db,DBMessage

def addSpecialMsg():

    specialMsgFile = open('specialMsg.txt',mode='r')
    specialMsgStr = specialMsgFile.read()
    specialMsgFile.close()

    messageObj = DBMessage(id=1,message= specialMsgStr, messageExists= 1)
    db.session.add(messageObj)
    db.session.commit()

    