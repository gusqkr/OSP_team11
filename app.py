from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys
import os

basedir = os.path.abspath(os.path.dirname(__file__))
application = Flask(__name__)
application.config['SECRET_KEY'] = "helloosp"

DB = DBhandler()

@application.route('/')
def home():
    return render_template('index.html')

@application.route('/list')
def view_list():
    page = request.args.get("page", 1, type=int)
    per_page = 9

    items = DB.get_items()

    if items :
        item_keys = list(items.keys())
        total_count = len(item_keys)
        last_page_num = (total_count - 1) // per_page + 1
        start_idx = (page - 1) * per_page
        end_idx = page * per_page
        page_item_keys = item_keys[start_idx:end_idx]
        page_items = {key: items[key] for key in page_item_keys}
    else:
        page_items = {}
        last_page_num = 1

    return render_template('list.html', items=page_items, page=page, last_page_num=last_page_num)


@application.route('/review')
def view_review():
    return render_template('review.html')

@application.route('/reg_items')
def reg_item():
    if 'id' not in session:
        flash("로그인 후 상품 등록 가능합니다.")
        return redirect(url_for('login'))
    return render_template('reg_items.html')

@application.route('/reg_reviews')
def reg_review():
    return render_template('reg_reviews.html')

@application.route('/qna')
def view_qna():
    return render_template('qna.html')

# @application.route('/submit_item')
# def reg_item_submit():
    name=request.args.get('name')
    seller=request.args.get('seller')
    addr=request.args.get('addr')
    email=request.args.get('email')
    category=request.args.get('category')
    card=request.args.get('card')
    status=request.args.get('status')
    phone=request.args.get('phone')

    print(name, seller, addr, email, category, card, status, phone)
    return render_template('reg_items.html')

@application.route('/submit_item_post', methods=['POST'])
def reg_item_submit_post():

    if 'id' not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for('login'))
    
    try:
        data = {
            "name": request.form.get('name'),
            "price": request.form.get('price'),
            "description": request.form.get('description'),
            "seller": session.get('id'),
            "addr": request.form.get('addr'),
            "email": request.form.get('email'),
            "category": request.form.get('category'),
            "card": request.form.get('card'),
            "status": request.form.get('status'),
            "phone": request.form.get('phone')
        }

        f = request.files.get('image')

        img_filename = ""

        if f and f.filename:
            filename = f.filename
            temp_path = os.path.join(basedir, 'static', 'images', filename)
            f.save(temp_path)

            img_filename = filename

        DB.insert_item(data, img_filename)

        flash("상품이 등록되었습니다.")
        return redirect(url_for('view_list'))
    
    except Exception as e:
        flash(f"상품 등록 중 오류 발생: {e}")
        return redirect(url_for('reg_item'))
    

@application.route("/view_detail/<item_key>")
def view_item_detail(item_key):
    item = DB.get_item_by_key(item_key)

    if item:
        return render_template("view_detail.html", item=item, key=item_key)
    else:
        flash("해당 상품을 찾을 수 없습니다.")
        return redirect(url_for('view_list'))
    
 
@application.route("/login")
def login():
    return render_template("user_login.html")

@application.route("/login_confirm",methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash=hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")
        return render_template("user_login.html")
    
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))

@application.route("/signup")
def signup():
    return render_template("user_signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("user_login.html")
    else:
        flash("user id already exist!")
        return render_template("user_signup.html")

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')
