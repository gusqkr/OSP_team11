import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.storage = firebase.storage()
    
    def insert_item(self, data, img_path):
        item_info = {
            "name": data['name'],
            "price": data['price'],
            "description": data['description'],
            "seller": data['seller'],
            "addr": data['addr'],
            "email": data['email'],
            "category": data['category'],
            "card": data['card'],
            "status": data['status'],
            "phone": data['phone'],
            "img_path": img_path
        }
        self.db.child("items").push(item_info)
        print(data, img_path)
        return True
    
    def get_items(self):
        items = self.db.child("items").get().val()
        return items
    
    def get_item_by_key(self, key):
        item_data = self.db.child("items").child(key).get().val()
        return item_data
    
    def insert_user(self, data, pw):
        user_info = {
            "id": data['id'],
            "pw": pw,
            "nickname": data['nickname']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print("New user added:", data)
            return True
        else:
            print("User ID already exists:", data['id'])
            return False

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        print("users###", users.val())
        if users.val() is None:
            return True
        else:
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return False
            return True
    
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return True
        return False
    
    def reg_review(self, data, img_path):
        review_info = {
            "title": data['title'],
            "rate": data['reviewStar'],
            "review": data['reviewContents'],
            "img_path": img_path
        }
        self.db.child("review").child(data['name']).set(review_info)
        return True

    def get_heart_byname(self, uid, item_key):
        hearts = self.db.child("heart").child(uid).get()

        if hearts.val() is None:
            return None

        for res in hearts.each():
            if res.key() == item_key:
                return res.val()

        return None

    def update_heart(self, user_id, isHeart, item_key):
        heart_info = {
            "interested": isHeart
        }

        self.db.child("heart").child(user_id).child(item_key).set(heart_info)
        return True

    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        return reviews
    
    def get_review_byname(self, item_name):
        review = self.db.child("review").child(item_name).get().val()
        return review