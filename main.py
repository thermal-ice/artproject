from flask import Flask, redirect, url_for, render_template, request
from gSheets import GSheets
import datetime



# Constants
password = "[Redacted for github]"
numberOfCandles = 20

# Fields
app = Flask(__name__)
sheets = GSheets()



# Routes
@app.route('/')
@app.route('/home')
def home():
    existsList = sheets.getMsgExistsList()
    return render_template('home.html', litCandlesList=existsList, rowNum=5)


@app.route('/candleread', methods=['POST', 'GET'])
def candleread():
    if request.method != "POST":
        return redirect(url_for('home'))

    # Check if its the special message
    if request.form.get('candleNum') == "SM":
        return render_template('candleread.html', msg= sheets.getSpecialMsg())


    currIndex = int(request.form.get('candleNum'))

    # ids start from 1
    msg = sheets.getMessage(candleNum=currIndex+1)
    return render_template('candleread.html', msg=msg)


@app.route('/candlewrite', methods=['POST', 'GET'])
def candlewrite():
    if request.method == "POST":
        candleNum = int(request.form.get('candleNum'))
        return render_template('candlewrite.html', candleNum=candleNum)

    return redirect(url_for('home'))


@app.route('/writeValues', methods=["POST"])
def writeValues():
    currIndex = int(request.form.get('index'))
    currMsg = request.form.get('msg')

    writeResultSuccessful = sheets.addMsg(message=currMsg,candleNum=currIndex + 1)

    if not writeResultSuccessful:
        return redirect(url_for('candlewriteerror'))


    return render_template('candleread.html', msg=currMsg)


# Handle it so it redirects to the already given message, or homepage
@app.route('/candlewriteerror')
def candlewriteerror():
    return render_template('candlewriteerror.html')


@app.route('/reset')
def reset():
    return render_template('reset.html', existsList=sheets.getMsgExistsList())


@app.route('/resetresult', methods=["POST"])
def resetresult():
    passwordAttempt = request.form.get('password')

    if (password != passwordAttempt):
        return render_template('resetresult.html', isSucc=False)
    else:

        if request.form.get('candleNum') == "All":
            sheets.resetAllMessages()
        else:
            # Its some number
            resetIndex = int(request.form.get('candleNum'))

            sheets.resetSingleMessage(candleNum= resetIndex + 1)

        return render_template('resetresult.html', isSucc=True)


@app.route('/about')
def about():
    return render_template('about.html')




# Main method
if __name__ == "__main__":
    app.run(debug=True)
