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
    fdb = TinyDB(r'C:\Users\sanya\Dekstop\CinemaExperience-aWebservicesEcosystem\allBookings\dbase\fooddb.json')
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
    mdb = TinyDB(r'C:\Users\sanya\Dekstop\CinemaExperience-aWebservicesEcosystem\allBookings\dbase\moviedb.json')
    userName = request.form["username"]
    mName, mQuant = request.form["name"], int(request.form["moviequant"])
    abc1 = {'username': userName, 'mname': mName, 'mquant': str(mQuant)}
    try:
        mdb.insert(abc1)
        return jsonify({"status": "OK"})
    except:
        return jsonify({"status": "FAILURE"})


@app.route("/api/foodorder/view", methods=['POST', 'GET'])
def viewfood(username):
    fdb = TinyDB(r'C:\Users\sanya\Dekstop\CinemaExperience-aWebservicesEcosystem\allBookings\dbase\fooddb.json')
    #userName = request.form["username"]
    User1 = Query()
    testing1= fdb.search(User1.username == 'admin')
    return jsonify(testing1)



@app.route("/api/movieticket/view", methods=['POST', 'GET'])
def viewmovie(username):
    # print(request.form)
    mdb = TinyDB(r'C:\Users\sanya\Dekstop\CinemaExperience-aWebservicesEcosystem\allBookings\dbase\moviedb.json')
    #userName = request.form["username"]
    User = Query()
    testing = mdb.search(User.username == 'admin')
    return jsonify(testing)


if __name__ == '__main__':
    app.run(debug=True, port=4500)
