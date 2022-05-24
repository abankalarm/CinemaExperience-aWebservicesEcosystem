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


@app.route("/viewfoodorder", methods=['POST', 'GET'])
def index2():
    # print(request.form)
    fdb = TinyDB(r'/dbase/fooddb.json')
    userName = str(request.form["username"])
    abc = {'username':userName, 'Popcorn': int(request.form["Popcorn"]), 'Coke': int(request.form["Coke"]),
           'Nachos': int(request.form["Nachos"])}
    #print(abc)
    fdb.insert(abc)
    User = Query()
    testing1= fdb.search(User.username == 'admin')
    # pendingOrders = {(k, v) for k, v in abc.items() if v > 0}
    # #print(pendingOrders)
    # if pendingOrders != set():
    # return render_template('viewOrder.html', abc=userName, it1q=abc['Popcorn'],
    #                            it2q=abc['Coke'], it3q=abc['Nachos'], db=abc)#, po=pendingOrders)
    # # else:
    # #     return render_template('Error.html')
    return jsonify(testing1)

@app.route("/viewmovieticket", methods=['POST', 'GET'])
def index3():
    # print(request.form)
    mdb = TinyDB(r'/dbase/moviedb.json')
    userName = request.form["username"]
    mName, mQuant = request.form["name"], int(request.form["moviequant"])
    abc1 = {'username': userName, 'mname': mName, 'mquant': str(mQuant)}
    mdb.insert(abc1)
    User = Query()
    testing = mdb.search(User.username == 'admin')
    return jsonify(testing)
    #print(testing)
    # if mQuant > 0:
    #     return render_template('viewBooking.html', abc=userName, mn=mName, mq=mQuant,db=abc1, db1=testing)
    # else:
    #     return render_template('Error.html')


if __name__ == '__main__':
    app.run(debug=True)
