from flask import request, jsonify
from vikingapp import app
from vikingapp.mod.first_ext import FirstExt

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/name/<string:name>', methods=['GET'])
def greet_person(name):
    return f"Hello {name}!"

@app.route('/sum', methods=['GET'])
def sum_stuff():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    return jsonify({'x': x, 'y': y, 'sum': FirstExt(x,y).some_method()})
