from flask import Flask, render_template, request, flash, redirect, url_for, session,jsonify
from main_db import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.secret_key = "SUPERSECRET"

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
    return render_template('login.html', login_failed=False)

@application.route('/login_confirm',methods=['POST'])
def login_confirm():
    id = request.form.get("id")
    pw = request.form.get("pw")
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    
    if not DB.verify_user(id, pw_hash): #user정보 없으면 false 
        return render_template("login.html", login_failed=True)

    session["id"] = id #세션에 id 저장 
    return redirect(url_for("home")) #이후 수정 필요

@application.route('/logout')
def logout():
    session.clear()
    return render_template('login.html') #이후 수정 필요
@application.route('/signup')
def signup():
    return render_template('signup.html')

@application.route("/signup_confirm", methods=["POST"])
def signup_confirm():
    data = request.form
    pw = data.get("pw")
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    
    if DB.insert_user(data, pw_hash):
        return render_template("login.html") 
    else: 
        flash("insert_data 실패")
        return render_template("signup.html")
    
@application.route("/check_id", methods=["POST"])
def check_id():
    user_id = request.form.get("id")
    if DB.user_duplicate_check(user_id): #중복확인
        return jsonify({"available": True, "message": "사용 가능한 아이디입니다."})
    else:
        return jsonify({"available": False, "message": "이미 사용 중인 아이디입니다."})

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
    
@application.route('/qna')
def view_qna():
    return render_template('qna.html') #수정

@application.route('/product_detail')
def view_product_detail():
    return render_template('product_detail.html') 

@application.route('/review_detail')
def view_reiview_detail():
    return render_template('review_detail.html') 


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5001)
