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

catalog_url = "http://c2.rehacks.live:8000"

@app.route("/soap", methods=['POST', 'GET'])
def soapcatalog():
    user = str(request.form["username"])
    movietype = int(request.form["mtype"])
    c = Client(catalog_url+'/?wsdl')
    catalog = c.service.say_hello('movie', movietype)[0]
    return render_template('makeBooking.html', user = user, catalog=catalog, message = "")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port = 80)