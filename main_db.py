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
        
    def get_all_items(self): #이후에 구매한 item목록가져오는 걸로 수정(write_review)
        items = self.db.child("items").get().val() 
        if not items:
            return []
        result = []
        for item_id, data in items.items():
            data["id"] = item_id         
            result.append(data)
        return result
    
    def insert_review(self, data, img_path):
        item = self.db.child("items").child(data['item_id']).get().val()
        review = {
            "user_id": data['user_id'],
            "item_id": data['item_id'],
            "item_name": item['name'],
            "title": data['title'],
            "content": data['content'],
            "rating": data['rating'],
            "img_path": img_path
        }
        self.db.child("reviews").child(item['name']).set(review) #set -> 물건당 리뷰한개 
        return True    
    
    def get_all_reviews(self):
        reviews = self.db.child("reviews").get().val()
        return reviews
    
    def get_review(self, review_id):
        # review_id = insert_review에서 사용한 item['name'] = 상품이름
        return self.db.child("reviews").child(review_id).get().val()

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
    
    def get_heart_count(self, product_name):
        users = self.db.child("user").get().val()
        count = 0
        if users:
            for user_id, user_data in users.items():
                hearts = user_data.get("hearts", [])
                if 'heart' in user_data and product_name in user_data['heart']:
                    count += 1
        return count
    
    def toggle_heart(self, user_id, product_name):
        heart_item = self.db.child("user").child(user_id).child("heart").child(product_name).get().val()

        if heart_item:
            self.db.child("user").child(user_id).child("heart").child(product_name).remove()
            return False
        else:
            item_info = self.db.child("items").child(product_name).get().val()

            heart_data = {
                "img_path": item_info['img_path'],
                "name": item_info['name'],
                "price": item_info['price'],
                "seller": item_info['seller']
            }
            self.db.child("user").child(user_id).child("heart").child(product_name).set(heart_data)
            return True
        
    def is_hearted(self, user_id, product_name):
        heart_item = self.db.child("user").child(user_id).child("heart").child(product_name).get().val()
        return True if heart_item else False
    
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
