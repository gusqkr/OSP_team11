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
    def update_password(self, user_id, new_pw):
        self.db.child("user").child(user_id).update({"pw":new_pw})
        return True
    
    def insert_review(self, item_id, data, img_path):
        item = self.db.child("items").child(item_id).get().val()
        if not item:
            print(f"ERROR: Item with ID {item_id} not found for review.")
            return False
        review = {
            "user_id": data['user_id'],
            "item_id": item_id,
            "item_name": item['name'],
            "title": data['title'],
            "content": data['content'],
            "rating": data['rating'],
            "img_path": img_path
        }
        self.db.child("reviews").child(item_id).set(review) #set -> 물건당 리뷰한개 
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
            "img_path": img_path,
            "heart_count" : 0,
            "buyer" : "",
            "selling_status" : "selling"
        }
        self.db.child("items").push(item_info)
        return True
    
    def get_items_selling(self): #selling_status=="selling"인 상품만  get
        items = self.db.child("items").get().val()
        if not items:
            return {} 
        
        selling_items = {}
        for item_id, data in items.items():
            if data.get("selling_status") == "selling":   
                selling_items[item_id] = data   
        return selling_items
    
    def get_item_detail(self, name):
        item = self.db.child("items").child(name).get().val()
        return item
    
    def get_heart_count(self, product_id): #아이템의 찜수 가져오기
        item = self.db.child("items").child(product_id).get().val()
        if not item:
            return 0
        heart_count = item.get("heart_count", 0)
        try:
            return int(heart_count)
        except (TypeError, ValueError):
            return 0

    def is_hearted(self, user_id, product_id): # 사용자가 해당 상품을 찜했는지 확인
        hearted_items = self.db.child("user").child(user_id).child("heart").get().val()
        if not hearted_items:
            return False
        return product_id in hearted_items
    def add_heart(self, user_id, product_id): #사용자 db에 heart 목록 추가, 상품 db에 count+1
        self.db.child("user").child(user_id).child("heart").child(product_id).set(True)
        
        current_count = self.get_heart_count(product_id)
        new_count = current_count + 1
        self.db.child("items").child(product_id).update({"heart_count": new_count})
        
        return True
    def remove_heart(self, user_id, product_id):
        self.db.child("user").child(user_id).child("heart").child(product_id).remove()
        
        current_count = self.get_heart_count(product_id)
        new_count = max(0, current_count - 1) 
        self.db.child("items").child(product_id).update({"heart_count": new_count})
        return True
    
    def get_user_hearted_items(self, user_id): #사용자가 찜한 모든 상품 id
        return self.db.child("user").child(user_id).child("heart").get().val()
    
    def get_hearted_items_details(self, user_id): #사용자가 찜한 상품의 상세정보
        hearted_items = self.db.child("user").child(user_id).child("heart").get().val()
        if not hearted_items:
            return {}
        
        items_detail = {}
        for item_id in hearted_items.keys():
            item = self.db.child("items").child(item_id).get().val()
            if item: 
                items_detail[item_id] = item
        
        return items_detail
    
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
    def purchase_product(self, buyer_id, product_id): #구매 처리함수 
        item = self.db.child("items").child(product_id).get().val()
        if not item:
            return False
        if item.get("buyer"):
            return False
        
        update_data = {
            "buyer": buyer_id,
            "selling_status": "sold"
        }
        self.db.child("items").child(product_id).update(update_data)
        purchase_data = {
            "item_id": product_id,
            "name": item["name"]
        }
        self.db.child("user").child(buyer_id).child("purchases").child(product_id).set(purchase_data)
        return True
    def get_user_purchases(self, user_id): #리뷰를 위한 구매목록 가져오기 
        purchases = self.db.child("user").child(user_id).child("purchases").get().val()
        if not purchases:
            return []
        
        result = []
        for item_id, data in purchases.items():
            if self.has_review_by_user(user_id, item_id):
                continue
            data["id"] = item_id
            result.append(data)
        return result   
    def has_review_by_user(self, user_id, item_id):
        reviews = self.db.child("reviews").get().val()
        if not reviews:
            return False

        for _, rev in reviews.items():
            # insert_review 에서 넣어둔 필드 기준
            if rev.get("user_id") == user_id and rev.get("item_id") == item_id:
                return True

        return False
    
    # 마이페이지에 필요한 정보
    def get_my_selling_items(self, user_id): #내가 올린 물건
        items = self.db.child("items").get().val()
        if not items:
            return {}
        
        my_items = {}
        for item_id, data in items.items():
            if data.get("seller") == user_id:
                my_items[item_id] = data
        return my_items

    def get_my_purchased_items_details(self, user_id): #내가 구매한 상품 정보
        purchases = self.db.child("user").child(user_id).child("purchases").get().val()
        if not purchases:
            return {}
        
        purchased_items = {}
        for item_id in purchases.keys():
            item_detail = self.db.child("items").child(item_id).get().val()
            if item_detail:
                purchased_items[item_id] = item_detail
                
        return purchased_items

    def get_my_reviews(self, user_id): #내가 쓴 리뷰 정보
        all_reviews = self.db.child("reviews").get().val()
        if not all_reviews:
            return {}
            
        my_reviews = {}
        for review_id, data in all_reviews.items():
            if data.get("user_id") == user_id:
                my_reviews[review_id] = data
        return my_reviews