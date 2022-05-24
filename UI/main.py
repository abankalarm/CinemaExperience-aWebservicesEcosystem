from email import message
import json
from os import access
from urllib import request
from flask import *
import requests


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


@app.route("/viewfoodorder", methods=['POST', 'GET'])
def index2():
    # print(request.form)
    userName = request.form["username"]
    abc = {'Popcorn': int(request.form["Popcorn"]), 'Coke': int(request.form["Coke"]),
           'Nachos': int(request.form["Nachos"])}
    pendingOrders = {(k, v) for k, v in abc.items() if v > 0}
    if pendingOrders != set():
        return render_template('viewOrder.html', abc=userName, it1q=abc['Popcorn'],
                               it2q=abc['Coke'], it3q=abc['Nachos'], po=pendingOrders)
    else:
        return render_template('Error.html')


@app.route("/viewmovieticket", methods=['POST', 'GET'])
def index3():
    # print(request.form)
    userName = request.form["username"]
    mName, mQuant = request.form["name"], int(request.form["moviequant"])
    if mQuant > 0:
        return render_template('viewBooking.html', abc=userName, mn=mName, mq=mQuant)
    else:
        return render_template('Error.html')


if __name__ == '__main__':
    app.run(debug=True, port = 4000)
