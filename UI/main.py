from email import message
import json
from os import access
from urllib import request
from flask import *
import requests
from tinydb import TinyDB, Query


app = Flask(__name__)

authservice_url = "http://127.0.0.1:5000"
booking_url = "http://127.0.0.1:4500"


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('login.html', message = "")


@app.route("/login", methods=['POST', 'GET'])
def index1():
    username = request.form['username']
    password = request.form['password']
    response = requests.post(authservice_url + '/login', data = {'username':username, 'password' : password})
    response = response.json()
    try:
        if(len(response["access_token"])>10):
            access_token = response["access_token"]
            print("got here")
            refresh_token = response["refresh_token"]
            print("got here")
            message = response["message"]
            print("got here")
            return render_template('homePage.html', access_token = response["access_token"], refresh_token = response["refresh_token"], message = response["message"])
    except:    
        return render_template('login.html', message = "Login failed")

@app.route("/register", methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    response = requests.post(authservice_url + '/registration', data = {'username':username, 'password' : password})
    response = response.json()
    print(response)
    try:
        if(len(response["access_token"])>10):
            return render_template('homePage.html', access_token = response["access_token"], refresh_token = response["refresh_token"], message = response["message"])
    except:    
        return render_template('login.html', message = "Login failed")

@app.route("/logout", methods=['POST'])
def logout():
    jwt = request.form['jwt']
    headers = {'Authorization': 'Bearer '+jwt}
    response = requests.post(authservice_url + '/logout/access', headers=headers)
    response = response.json()
    print(response)
    return render_template('login.html', message = response)

@app.route("/bookOrOrder", methods=['POST', 'GET'])
def index1():
    if request.form['choosing'] == 'food':
        return render_template('makeOrder.html')
    elif request.form['choosing'] == 'movie':
        return render_template('makeBooking.html')

@app.route("/viewfoodorder", methods=['POST', 'GET'])
def index2():
    fdb = TinyDB(r'/UI/dbase/fooddb.json')  # HANDLE ADDRESS LATER ON
    userName = str(request.form["username"])
    abc = {'username':userName, 'Popcorn': int(request.form["Popcorn"]), 'Coke': int(request.form["Coke"]),
           'Nachos': int(request.form["Nachos"])}
    #print(abc)
    fdb.insert(abc)
    User = Query()
    testing1= fdb.search(User.username == userName)
    return jsonify(testing1)


# @app.route("/movie/buy", methods=['POST'])
# def index3():
#     username = request.form["username"]
#     mName, mQuant = request.form["name"], int(request.form["moviequant"])
#     if mQuant > 0:
#         return render_template('viewBooking.html', abc=username, mn=mName, mq=mQuant)
#     else:
#         return render_template('Error.html')


@app.route("/viewmovieticket", methods=['POST', 'GET'])
def index3():
    mdb = TinyDB(r'/UI/dbase/moviedb.json')   # HANDLE ADDRESS LATER ON
    userName = request.form["username"]
    mName, mQuant = request.form["name"], int(request.form["moviequant"])
    abc1 = {'username': userName, 'mname': mName, 'mquant': str(mQuant)}
    mdb.insert(abc1)
    User = Query()
    testing = mdb.search(User.username == userName)
    return jsonify(testing)

##  viewBooking.html and viewOrder.html are currently not being used

if __name__ == '__main__':
    app.run(debug=True, port = 4000)
