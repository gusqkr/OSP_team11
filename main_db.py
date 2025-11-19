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