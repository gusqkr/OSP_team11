from flask import Flask, render_template, request, flash, redirect, url_for, session,jsonify
from main_db import DBhandler
import hashlib
import sys
import math
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
def view_product():

    per_page = 15
    page = request.args.get('page', 1, type=int)

    items = DB.get_items()

    if items:
        item_list = list(items.items())

        total_items = len(item_list)
        total_pages = math.ceil(total_items / per_page)

        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        current_items = item_list[start_index:end_index]

        for item in current_items:
            name = item[0]
            data = item[1]
            heart_count = DB.get_heart_count(name)
            data['heart_count'] = heart_count
            
    else:
        current_items = []
        total_pages = 1

    return render_template('All_product.html', 
                           items=dict(current_items),
                           page=page, 
                           total_pages=total_pages,
                           total_items=len(items) if items else 0)

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

@application.route('/register_product', methods=['GET', 'POST'])
@application.route('/submit_item_post', methods=['POST'])
def register_product():

    if "id" not in session:
        return redirect(url_for("login", next="register_product", need_login=1))
    
    if request.method == 'POST':
        image_file = request.files.get("file")
        if image_file:
            image_file.save("static/images/{}".format(image_file.filename))
            img_path = "static/images/{}".format(image_file.filename)
        else:
            img_path = "static/images/default.png" #기본 이미지로 등록

        data = request.form

        product_name = data['name']
        seller = data['seller']
        addr = data['addr']
        status = data['status']
        price = data['price']
        description = data['description']

        item_data = {
            'seller': seller,
            'addr': addr,
            'status': status,
            'price': price,
            'description': description,
        }

        DB.insert_item(product_name, item_data, img_path)

        return redirect(url_for('view_product'))

    return render_template('product_register.html')

@application.route('/reg_question/<name>', methods=['POST'])
def reg_question(name):
    if "id" not in session:
        return redirect(url_for("login", next="view_product_detail", need_login=1))
    
    current_item = DB.get_item_detail(str(name))
    data = request.form.get('question')

    qna_data = {
        "writer": session["id"],
        "question": data,
        "answer": "",
        "product_name": current_item['name'],
        "img_path": current_item['img_path']
    }

    DB.write_question(name, qna_data)
    return redirect(url_for('view_product_detail', name=name)) 

@application.route('/reg_answer/<name>/<id>', methods=['POST'])   
def reg_answer(name, id):
    if "id" not in session:
        return redirect(url_for("login", next="view_qna", need_login=1))
    
    answer = request.form.get('answer_text')

    DB.write_answer(name, id, answer)

    return redirect(url_for('view_qna'))

@application.route('/qna_list')
def view_qna():
    all_qna = DB.get_all_questions()

    return render_template('qna_list.html', qna_list=all_qna) 

@application.route('/product_detail/<name>')
def view_product_detail(name):
    data = DB.get_item_detail(str(name))
    qna_data = DB.get_questions(str(name))
    count = DB.get_heart_count(str(name))
    return render_template('product_detail.html', name=name, data=data, qna=qna_data, count=count) 


@application.route('/show_heart/<name>', methods=['GET'])
def show_heart(name):
    if "id" not in session:
        return jsonify({'result': 'login_required'})
    
    user_id = session["id"]
    DB.toggle_heart(user_id, name)
    count = DB.get_heart_count(name)
    return jsonify({"result": "success", "count": count})




if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5001)
