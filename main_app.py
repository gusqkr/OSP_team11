from flask import Flask, render_template, request, flash, redirect, url_for, session
from main_db import DBhandler
import hashlib
import sys

application = Flask(__name__)

DB = DBhandler()

@application.route('/')
def home():
    return render_template('base.html') #수정

@application.route('/myheart')
def view_heart():
    return render_template('myheart.html') 

@application.route('/mypage')
def view_mypage():
    return render_template('mypage.html') 

@application.route('/login')
def login():
    return render_template('login.html')

@application.route('/signup')
def signup():
    return render_template('signup.html')

@application.route('/product')
def view_proudct():
    return render_template('All_product.html')

@application.route('/review')
def view_review():
    return render_template('review_list.html')

@application.route('/write_review')
def write_review():
    return render_template('Write_review.html')

@application.route('/register_product')
def register_product():
    return render_template('product_register.html')
    
@application.route('/qna_list')
def view_qna():
    return render_template('qna_list.html') 

@application.route('/product_detail')
def view_product_detail():
    return render_template('product_detail.html') 

@application.route('/review_detail')
def view_reiview_detail():
    return render_template('review_detail.html') 


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5001)
