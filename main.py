from flask import Flask, redirect,url_for,render_template, request
from flask_sqlalchemy import SQLAlchemy
from messageStore import MessageStore
from MessageStoreArray import MessageStoreArray
import datetime
# from DBMessageStore import DBMessage, db


#Constants
password = "[some super secret password that shall not be displayed on github]"
numberOfCandles = 20
specialLanternIndex = 0

#Fields
app = Flask(__name__)


#App configs

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # Three forward slashes indicates relative path

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #Something to do with peformance idk lol


db = SQLAlchemy(app)


def rowExists(index):
    return db.session.query(DBMessage).filter_by(id=index+1).scalar() is not None


def dataBaseRowsExistsToList():
    existsList = []

    #First message is the special message
    for i in range(numberOfCandles):
        # existsList.append(DBMessage.query.get(i+1) is not None)
       existsList.append(rowExists(index = i))

    return existsList



class DBMessage(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    message = db.Column(db.String, nullable= True) #Can make it null
    messageExists = db.Column(db.Integer,nullable= False)

    #Returns the string representation of the object
    def __repr__(self):
        return f"DBMessage('{self.message}','{self.messageExists}')"

class Resets(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    indicesReset = db.Column(db.String, nullable= False)
    timeReset = db.Column(db.DateTime, nullable=False,default=datetime.datetime.today)

#Routes
@app.route('/')
@app.route('/home')
def home():
    existsList = dataBaseRowsExistsToList()
    return render_template('home.html',litCandlesList = existsList,rowNum=5, specialMsgIndex = specialLanternIndex)



@app.route('/candleread', methods=['POST','GET'])
def candleread():
    if request.method !="POST":
        return redirect(url_for('home'))
    currIndex = int(request.form.get('candleNum'))

    #ids start from 1
    msg = DBMessage.query.get(currIndex+1).message
    return render_template('candleread.html',msg = msg)


@app.route('/candlewrite', methods = ['POST','GET'])
def candlewrite():

    if request.method=="POST":
        candleNum = int(request.form.get('candleNum'))
        return render_template('candlewrite.html',candleNum= candleNum)
     

    return redirect(url_for('home'))

@app.route('/writeValues', methods=["POST"])
def writeValues():
    currIndex = int(request.form.get('index'))
    currMsg = request.form.get('msg')

    if rowExists(currIndex):
        return redirect(url_for('candlewriteerror'))

    newMsg = DBMessage(id=currIndex+1, message= currMsg,messageExists=1)
    db.session.add(newMsg)
    db.session.commit()

    return render_template('candleread.html',msg = currMsg)


#Handle it so it redirects to the already given message, or homepage
@app.route('/candlewriteerror')
def candlewriteerror():
    return render_template('candlewriteerror.html')



@app.route('/reset')
def reset():
    return render_template('reset.html', existsList=dataBaseRowsExistsToList(),specialMsgIndex = specialLanternIndex)


@app.route('/resetresult', methods=["POST"])
def resetresult():

    passwordAttempt = request.form.get('password')
    resetedList = []


    if(password != passwordAttempt):
        return render_template('resetresult.html', isSucc= False)
    else:
        
        if request.form.get('candleNum') == "All":
            # listOfCandles.resetAllMsgStores()
            for i in range(numberOfCandles):
                if i == specialLanternIndex:
                    #Do not reset the special candle
                    continue
                else:
                    resetedList.append(i)
                    DBMessage.query.filter_by(id= i+1).delete()       

        else:
            resetIndex = int(request.form.get('candleNum'))
            # listOfCandles.resetMsgStoreAtIndex(resetIndex)
            resetedList.append(resetIndex)
            DBMessage.query.filter_by(id=resetIndex +1).delete()
        
        resetListObj = Resets(indicesReset= str(resetedList))
        db.session.add(resetListObj)

        db.session.commit()
        
        return render_template('resetresult.html',isSucc= True)
    

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resetTimes')
def resetTimes():
    return render_template('resetTimes.html',table= Resets.query.all())


#Main method
if __name__=="__main__":
    app.run(debug=True)