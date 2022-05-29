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
            refresh_token = response["refresh_token"]
            message = response["message"]
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
def choice():
    if request.form['choosing'] == 'food':
        return render_template('makeOrder.html')
    elif request.form['choosing'] == 'movie':
        return render_template('makeBooking.html')


@app.route("/insertfoodorder", methods=['POST', 'GET'])
def insertfood():
    viewfoodresult=request.form('/api/foodorder/view')
    return render_template('viewOrder.html')


@app.route("/insertmovieticket", methods=['POST', 'GET'])
def insertfticket():
    viewmovieresult=request.form()
    return render_template('viewBooking.html')


@app.route("/viewfoodorder", methods=['POST', 'GET'])
def viewfood():
    viewfoodresult=request.form('/api/foodorder/view')
    return render_template('viewOrder.html')


@app.route("/viewmovieticket", methods=['POST', 'GET'])
def viewticket():
    viewmovieresult=request.form()
    return render_template('viewBooking.html')

##  viewBooking.html and viewOrder.html are currently not being used

if __name__ == '__main__':
    app.run(debug=True, port = 4000)
