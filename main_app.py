from flask import Flask, render_template, request, flash, redirect, url_for, session,jsonify
from main_db import DBhandler
import hashlib
import sys
from datetime import timedelta
import math

application = Flask(__name__)
application.secret_key = "SUPERSECRET"
application.permanent_session_lifetime = timedelta(days=1)  # 자동 로그인 기간 (1일)

DB = DBhandler()

@application.route('/')
def home():
    return render_template('base.html') #수정

@application.route('/myheart')
def view_heart():
    if "id" not in session:
        return redirect(url_for("login", next="view_heart", need_login=1))
    return render_template('myheart.html') 

@application.route('/mypage')
def view_mypage():
    if "id" not in session:
        return redirect(url_for("login", next="view_mypage", need_login=1)) #로그인 후 mypage로 redirect
    return render_template('mypage.html') 

#로그인/로그아웃/회원가입
@application.route('/login')
def login():
    next_page = request.args.get("next")
    need_login = request.args.get("need_login") == "1"
    return render_template('login.html', login_failed=False, next_page=next_page, need_login=need_login)

@application.route('/login_confirm',methods=['POST'])
def login_confirm():
    id = request.form.get("id")
    pw = request.form.get("pw")
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    remember = request.form.get("remember") 
    
    if not DB.verify_user(id, pw_hash): #user정보 없으면 false 
        return render_template("login.html", login_failed=True)

    session["id"] = id #세션에 id 저장 
    
    if remember : 
        session.permanent = True
    else: 
        session.permanent = False
        
    next_page = request.form.get("next")
    return redirect(url_for(next_page)) if next_page else redirect(url_for("home"))
    #return redirect(url_for("home")) #이후 수정 필요

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

#리뷰
@application.route('/review')
def view_review():
    per_page = 8   
    page = request.args.get('page', 1, type=int)
    reviews = DB.get_all_reviews() 
    
    if reviews:
        review_list = list(reviews.items())   
        total_reviews = len(review_list)

        total_pages = math.ceil(total_reviews / per_page)

        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        current_reviews = review_list[start_index:end_index]
    else:
        current_reviews = []
        total_pages = 1
        total_reviews = 0

    return render_template(
        'review_list.html',
        reviews=dict(current_reviews),  
        page=page,
        total_pages=total_pages,
        total_reviews=total_reviews
    )

@application.route('/write_review')
def write_review():
    if "id" not in session:
        return redirect(url_for("login", next="write_review", need_login=1))
    author = session.get("id") #사용자 id
    items = DB.get_all_items() #이후 수정(구매 목록으로만)
    return render_template('Write_review.html', author=author,items=items)

@application.route('/write_review/<item_id>', methods=['POST'])
def wirte_review_init(item_id):
    user_id=session["id"]
    data = request.form
    image_file=request.files["image"]
    image_file.save("static/images/{}".format(image_file.filename))
    DB.insert_review(data,image_file.filename)
    return redirect(url_for('view_review'))

@application.route('/review_detail/<review_id>')
def view_review_detail(review_id):
    review = DB.get_review(review_id)

    return render_template('review_detail.html', review=review)   

@application.route('/register_product')
def register_product():
    return render_template('product_register.html')
    
@application.route('/qna_list')
def view_qna():
    return render_template('qna_list.html') 

@application.route('/product_detail')
def view_product_detail():
    return render_template('product_detail.html') 



if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5001)
