from flask import *

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('makeOrder.html')


@app.route("/vieworder", methods=['POST', 'GET'])
def index1():
    userName = request.form["username"]
    item1,item1Quant = request.form["item1"], request.form["item1Quantity"]
    item2,item2Quant = request.form["item2"], request.form["item2Quantity"]
    item3, item3Quant = request.form["item3"], request.form["item3Quantity"]
    return render_template('viewOrder.html', abc=userName, it1=item1, it2=item2, it3=item3, it1q=item1Quant, it2q=item2Quant, it3q=item3Quant)


# @app.route("/vieworder", methods=["POST", "GET"])
# def index1():
#     # if request.method == 'POST':
#     #     pass
#     # else:
#     return render_template('viewOrder.html')


if __name__ == '__main__':
    app.run(debug=True)
