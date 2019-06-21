from vikingapp import app

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/name/<string:name>', methods=['GET'])
def greet_person(name):
    return f"Hello {name}!"
