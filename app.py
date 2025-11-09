from flask import Flask, render_template, request
from database import DBhandler
import sys

application = Flask(__name__)

DB = DBhandler()

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

@application.route('/submit_item')
def reg_item_submit():
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
    image_file = request.files['file']
    image_file.save("static/images/{}".format(image_file.filename))
    data=request.form
    DB.insert_item(data['name'], data, image_file.filename)

    return render_template("result.html", data=data, img_path="static/images/{}".format(image_file.filename))
    """
    print ("\n=========== 입력받은 값 확인 ===========")
    print ("판매자 아이디 :", data['seller'])
    print ("상품 이름 :", data['name'])
    print ("주소 :", data['addr'])
    print ("카테고리 :", data['category'])
    print ("이메일 :", data['email'])
    print ("신용카드 여부 :", data['card'])
    print ("상품 상태 :", data['status'])
    print ("휴대폰 번호 :", data['phone'])
    print ("===============================================\n")
    """


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')
