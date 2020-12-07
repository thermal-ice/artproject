from flask import Flask, redirect,url_for,render_template, request
from messageStore import MessageStore
from MessageStoreArray import MessageStoreArray


#Constants
password = "[some fixed string]" #You tried. Just guess it and you'd probably get it right lol
specialLanternNum = 2

#Fields
app = Flask(__name__)
listOfCandles = MessageStoreArray(specialLanternNum= specialLanternNum)


@app.route('/')
@app.route('/home')
# @app.route('/home', methods = ['POST','GET'])
def home():
    # #Resets the current message
    # if request.method == "POST":
    #     currMsgStore.setLit(False)
    #     currMsgStore.setMsg("")
    #     return render_template("home.html",lit=currMsgStore.getIsLit())
    # else:
    #     return render_template("home.html", lit=currMsgStore.getIsLit())

    return render_template('home.html',msgStoreList= listOfCandles.getMsgStoreList(), rowNum= 5)



# @app.route('/candleread', methods=['POST','GET'])
# def candleread(index = -1):
#     if index != -1:
#         return render_template('candleread.html',msg= listOfCandles.getMsgStoreList()[index].getMsg())
#     elif request.method == "POST":
#         index = int(request.form['candleNum'])
#         return render_template('candleread.html',msg = listOfCandles.getMsgStoreList()[index].getMsg())
#     else:
#         return render_template('candleread.html', msg= currMsgStore.getMsg())


@app.route('/candleread', methods=['POST','GET'])
def candleread():
    if request.method !="POST":
        return redirect(url_for('home'))
    currIndex = int(request.form.get('candleNum'))
    return render_template('candleread.html',msg = listOfCandles.getMsgStoreList()[currIndex].getMsg())


@app.route('/candlewrite', methods = ['POST','GET'])
def candlewrite():

    #Error, someone has already submitted a message
    # if currMsgStore.getIsLit():
    #     return redirect(url_for('candlewriteerror'))

    
    if request.method=="POST":
        candleNum = int(request.form.get('candleNum'))
        return render_template('candlewrite.html',candleNum= candleNum)

    # if request.method == "POST":
    #     currMsgStore.setMsg(newMsg= request.form['nm'])
    #     currMsgStore.setLit(True)
    #     return redirect(url_for('candleread'))
    # if request.method == "POST":
    #     message = request.form['nm']
    #     index = int(request.form['candleNum'])
    #     listOfCandles.getMsgStoreList()[index].setMsg(message)
    #     return redirect(url_for('candleread',index= index))
     

    return redirect(url_for('home'))

@app.route('/writeValues', methods=["POST"])
def writeValues():
    currIndex = int(request.form.get('index'))
    currMsg = request.form.get('msg')

    currCandle = listOfCandles.getMsgStoreList()[currIndex]

    if currCandle.getIsLit():
        return redirect(url_for('candlewriteerror'))

    currCandle.setMsg(currMsg)
    currCandle.setLit(True)
    # return redirect(url_for('/displayMsg',index = currIndex))
    return render_template('candleread.html',msg = currCandle.getMsg())



#Handle it so it redirects to the already given message, or homepage
@app.route('/candlewriteerror')
def candlewriteerror():
    return render_template('candlewriteerror.html')


@app.route('/tabletest')
def tabletest():
    # if request.method == "POST":
    #     currMsgStore.setMsg(newMsg= request.form['candleNum'])
    #     currMsgStore.setLit(True)
    #     return render_template("home.html",lit=currMsgStore.getIsLit())
    # else:
    return render_template('tabletest.html',msgStoreList= listOfCandles.getMsgStoreList(), rowNum= 5)



@app.route('/reset')
def reset():
    return render_template('reset.html', candlesList=listOfCandles.getMsgStoreList())


@app.route('/resetresult', methods=["POST"])
def resetresult():

    passwordAttempt = request.form.get('password')

    if(password != passwordAttempt):
        return render_template('resetresult.html', isSucc= False)
    else:
        if request.form.get('candleNum') == "All":
            listOfCandles.resetAllMsgStores()
        else:
            resetIndex = int(request.form.get('candleNum'))
            listOfCandles.resetMsgStoreAtIndex(resetIndex)
        
        return render_template('resetresult.html',isSucc= True)
    

@app.route('/about')
def about():
    return render_template('about.html')

if __name__=="__main__":
    app.run(debug=True)