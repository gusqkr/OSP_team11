import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/main_auth.json') as f:
            config=json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.storage = firebase.storage()


    #user crud
    def insert_user(self, data, pw):
        user_info = {
            "id" : data['id'], 
            "pw" : pw,
            "email" : data['email'],
            "tel": data['tel']        
        }
        self.db.child("user").child(data['id']).set(user_info)
        return True

    def user_duplicate_check(self, user_id: str) -> bool:
        user_data = self.db.child("user").child(user_id).get().val()
        return user_data is None   #user_data=None이면 True
    
    def get_user(self, user_id):
        return self.db.child("user").child(user_id).get().val()
    
    def verify_user(self, user_id :str, pw: str):
        user = self.get_user(user_id)
        if not user: 
            return False
        
        if user.get('id')==user_id and user.get('pw')==pw :
            return True
        else: return False

    def insert_item(self, name, data, img_path):
        item_info = {
            "name": name,
            "seller":data['seller'],
            "addr": data['addr'],
            "status": data['status'],
            "price": data['price'],
            "description": data['description'],
            "img_path": img_path
        }
        self.db.child("items").push(item_info)
        return True
    
    def get_items(self):
        items = self.db.child("items").get().val()
        return items
    
    def get_item_detail(self, name):
        item = self.db.child("items").child(name).get().val()
        return item
    
    def write_question(self, product_name, data):
        self.db.child("questions").child(product_name).push(data)
        return True
    
    def get_all_questions(self):
        questions = self.db.child("questions").get().val()
        return questions
    
    def write_answer(self, product_name, question_id, answer):
        self.db.child("questions").child(product_name).child(question_id).update({"answer": answer})
        return True
    
    def get_questions(self, product_name):
        questions = self.db.child("questions").child(product_name).get().val()
        return questions