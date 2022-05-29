from email import message
from glob import glob
import json
from os import access
from urllib import request
from flask import *
import requests
from tinydb import TinyDB, Query
from suds.client import Client

app = Flask(__name__)

authservice_url = "http://127.0.0.1:5000"
booking_url = "http://127.0.0.1:4500"
catalog_url = "http://127.0.0.1:8000"

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
            refresh_token = response["refresh_token"]
            message = response["message"]
            return render_template('homePage.html', user = username, access_token = response["access_token"], refresh_token = response["refresh_token"], message = response["message"])
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


@app.route("/soap/catalog", methods=['POST', 'GET'])
def soapcatalog():
    user = str(request.form["username"])
    movietype = int(request.form["mtype"])
    c = Client(catalog_url+'/?wsdl')
    catalog = c.service.say_hello('movie', movietype)[0]
    return render_template('makeBooking.html', user = user, catalog=catalog, message = "")


@app.route("/bookOrOrder", methods=['POST', 'GET'])
def choice():
    user = request.form['username']
    if(user==""):
        return render_template('login.html')
    if request.form['choosing'] == 'food':
        return render_template('makeOrder.html', user = user, message = "")
    elif request.form['choosing'] == 'movie':
        return render_template('movietype.html', user = user)


@app.route("/insertfoodorder", methods=['POST', 'GET'])
def insertfood():
    userName = str(request.form["username"])
    abc = {'username':userName, 'Popcorn': int(request.form["Popcorn"]), 'Coke': int(request.form["Coke"]),
           'Nachos': int(request.form["Nachos"])}
    response = requests.post(booking_url + '/api/foodorder/insert', data = abc)
    print(response)
    message = response.json()
    return render_template('makeOrder.html', message=message, user = userName)

@app.route("/insertmovieticket", methods=['POST', 'GET'])
def insertticket():
    user = str(request.form["username"])
    mName, mQuant = request.form["name"], int(request.form["moviequant"])
    abc = {'username': user, 'mname': mName, 'mquant': str(mQuant)}
    print("THIS IS US")
    print(abc)
    response = requests.post(booking_url + '/api/movieticket/insert', data = abc)
    print(response)
    message = response.json()
    return render_template('makeBooking.html', message=message, user = user)


@app.route("/viewfoodorder", methods=['POST', 'GET'])
def viewfood():
    username = str(request.form["username"])
    abc = {'username':username}
    response = requests.post(booking_url + '/api/foodorder/view', data = abc)
    print(response.json())
    message = response.json()[0]
    print(message)
    return render_template('viewOrder.html', message=message, user = username, Popcorn = message['Popcorn'], Coke = message['Coke'], Nachos = message['Nachos'])


@app.route("/viewmovieticket", methods=['POST', 'GET'])
def viewticket():
    username = str(request.form["username"])
    abc = {'username':username}
    response = requests.post(booking_url + '/api/movieticket/view', data = abc)
    print(response)
    message = response.json()[0]
    print(message)
    return render_template('viewBooking.html', message=message, user = username, moviename = message['mname'], ticketquantity = message['mquant'])

##  viewBooking.html and viewOrder.html are currently not being used

if __name__ == '__main__':
    app.run(debug=True, port = 4000)
