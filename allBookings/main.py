from flask import *
from tinydb import TinyDB, Query

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('homePage.html')


@app.route("/bookOrOrder", methods=['POST', 'GET'])
def index1():
    if request.form['choosing'] == 'food':
        return render_template('makeOrder.html')
    elif request.form['choosing'] == 'movie':
        return render_template('makeBooking.html')


@app.route("/api/foodorder/insert", methods=['POST'])
def insertfood():
    fdb = TinyDB(r'allBookings/dbase/fooddb.json')
    userName = str(request.form["username"])
    abc = {'username':userName, 'Popcorn': int(request.form["Popcorn"]), 'Coke': int(request.form["Coke"]),
           'Nachos': int(request.form["Nachos"])}
    try:
        fdb.insert(abc)
        return jsonify({"status": "OK"})
    except:
        return jsonify({"status": "FAILURE"})


@app.route("/api/movieticket/insert", methods=['POST', 'GET'])
def insertmovie():
    mdb = TinyDB(r'allBookings/dbase/moviedb.json')
    userName = request.form["username"]
    mName, mQuant = request.form["mname"], int(request.form["mquant"])
    abc1 = {'username': userName, 'mname': mName, 'mquant': str(mQuant)}
    try:
        mdb.insert(abc1)
        return jsonify({"status": "OK"})
    except:
        return jsonify({"status": "FAILURE"})


@app.route("/api/foodorder/view", methods=['POST', 'GET'])
def viewfood():
    fdb = TinyDB(r'allBookings/dbase/fooddb.json')
    username = request.form["username"]
    User1 = Query()
    testing1= fdb.search(User1.username == username)
    return jsonify(testing1)



@app.route("/api/movieticket/view", methods=['POST', 'GET'])
def viewmovie():
    # print(request.form)
    mdb = TinyDB(r'allBookings/dbase/moviedb.json')
    username = request.form["username"]
    print("----------")
    print(username)
    User = Query()
    testing = mdb.search(User.username == username)
    return jsonify(testing)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4500)
