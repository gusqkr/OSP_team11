from flask import Flask, render_template
import sys

application = Flask(__name__)

@application.route('/')
def home():
    return render_template('index.html')

@application.route('/list')
def view_list():
    return render_template('list.html')

@application.route('/review')
def view_review():
    return render_template('review.html')

@application.route('/reg_items')
def reg_item():
    return render_template('reg_items.html')

@application.route('/reg_reviews')
def reg_review():
    return render_template('reg_reviews.html')

@application.route('/qna')
def view_qna():
    return render_template('qna.html')

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')