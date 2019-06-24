from flask import Flask
app = Flask(__name__)

import vikingapp.views

def main():
    app.run()

def init():
    if __name__ == '__main__':
        main()

init()
