from flask import *

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
    app.run(debug=True)
