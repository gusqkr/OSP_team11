from flask import Flask, render_template
import sys

application = Flask(__name__)

@application.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')