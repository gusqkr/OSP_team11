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
        self.db.child("reviews").child(item['name']).set(review)
        return True       