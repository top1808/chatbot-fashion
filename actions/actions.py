# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import Any, Dict, List, Text
from typing import Text
from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted

from utils.functionHelper import chose_size_from_height, get_all_name_products, get_all_name_categories, chose_shoes_size_from_foot_size, get_products_buy_name, get_all_name_discount_programs
from db_shop_connect import get_products_by_name

class ActionGetProducts(Action):
    def name(self):
        return "action_get_products"
    
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text=f"Chúng tôi bán những sản phẩm thời trang như {get_all_name_products()},... và nhiều sản phẩm khác nữa.")
        return []

class ActionGetCategories(Action):
    def name(self):
        return "action_get_categories"
    
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text=f"Chúng tôi bán những loại hàng như {get_all_name_categories()},... và nhiều loại hàng khác nữa.")
        return []  

class ActionGetDiscountPrograms(Action):
    def name(self):
        return "action_get_discount_programs"
    
    def run(self, dispatcher, tracker, domain):
        data = get_all_name_discount_programs()
        names = data["names"]
        products = data["products"]
        dispatcher.utter_message(text=f"Chúng tôi đang có những chương trình khuyến mãi như {names}. Bạn có thể tham khảo những sản phẩm giảm giá của những chương trình khuyến mãi này: ")
        for product in products:
            dispatcher.utter_message(text=f"{product['name']}")
            for image in product['images']:
                dispatcher.utter_message(image=image)
            dispatcher.utter_message(attachment=f"http://localhost:3000/product/{product['_id']}")
        return []       

class ActionResetCustHeight(Action):
    def name(self):
        return "action_reset_cust_height"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("cust_height", None)]

class ActionResetCustWeight(Action):
    def name(self):
        return "action_reset_cust_weight"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("cust_weight", None)]

class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text=f"Xin lỗi, tôi không hiểu ý bạn.")
        return [UserUtteranceReverted()]
    
class ActionGetProductByType(Action):
    def name(self):
        return "action_get_product_by_type"

    def run(self, dispatcher, tracker, domain):
        item_type = tracker.get_slot("item_type")
        products = get_products_by_name(item_type)
        print("item_type: ", item_type)
        if products:
            dispatcher.utter_message(text=f"Đây là 1 số loại {item_type} thích hợp để bạn chọn:")
            for product in products:
                dispatcher.utter_message(text=f"{product['name']}")
                for image in product['images']:
                    dispatcher.utter_message(image=image)
                dispatcher.utter_message(attachment=f"http://localhost:3000/product/{product['_id']}")
        else:
            dispatcher.utter_message(text=f"Xin lỗi chúng tôi không có sản phẩm này.")
        return []

class ActionCheckSize(Action):
    def name(self):
        return "action_check_size"

    def run(self, dispatcher, tracker, domain):
        cust_height = tracker.get_slot("cust_height")
        cust_weight = tracker.get_slot("cust_weight")
        if cust_height:
            get_size = chose_size_from_height(cust_height)
            if get_size:
                dispatcher.utter_message(text=f"Bạn cao {cust_height} và nặng {cust_weight} thì nên mặc size {get_size}.")
            else:
                dispatcher.utter_message(text=f"Xin lỗi chúng tôi không có size này. Vui lòng liên hệ với chúng tôi để đặt riêng.")
            
        else:
            dispatcher.utter_message(text=f"Xin lỗi tôi không biết chính xác size của bạn.")

        return []
    
class ActionCheckShoesSize(Action):
    def name(self):
        return "action_check_shoes_size"

    def run(self, dispatcher, tracker, domain):
        item_type = tracker.get_slot("item_type")
        print("item_type: ", item_type)
        products = get_products_by_name(item_type)
        if products:
            dispatcher.utter_message(text=f"Đây là 1 số loại {item_type} thích hợp để bạn chọn:")
            for product in products:
                dispatcher.utter_message(text=f"{product['name']}")
                for image in product['images']:
                    dispatcher.utter_message(image=image)
                dispatcher.utter_message(attachment=f"http://localhost:3000/product/{product['_id']}")
        else:
            dispatcher.utter_message(text=f"Xin lỗi chúng tôi không có sản phẩm này.")
       
        return []

class ActionCheckItemType(Action):
    def name(self):
        return "action_check_item_type"

    def run(self, dispatcher, tracker, domain):
        item_type = tracker.get_slot("item_type")
        products = get_products_by_name(item_type)
        if products:
            dispatcher.utter_message(text=f"Đây là 1 số loại {item_type} thích hợp để được chọn:")
            for product in products:
                dispatcher.utter_message(text=f"{product['name']}")
                for image in product['images']:
                    dispatcher.utter_message(image=image)
                dispatcher.utter_message(attachment=f"http://localhost:3000/product/{product['_id']}")
        else:
            dispatcher.utter_message(text=f"Xin lỗi chúng tôi không có sản phẩm này.")
        return []

class ValidateSizeForm(FormValidationAction):
    def name(self):
        return "validate_size_form"

    def validate_cust_height(self, slot_value, dispatcher, tracker, domain):
        return {"cust_height": slot_value}
    
    def validate_cust_weight(self, slot_value, dispatcher, tracker, domain):
        return {"cust_weight": slot_value}

class ValidateItemTypeForm(FormValidationAction):
    def name(self):
        return "validate_item_type_form"

    def validate_item_type(self, slot_value, dispatcher, tracker, domain):
        return {"item_type": slot_value}

class ValidateShoesSizeForm(FormValidationAction):
    def name(self):
        return "validate_shoes_size_form"

    def validate_foot_size(self, slot_value, dispatcher, tracker, domain):
        return {"foot_size": slot_value}
    
class ValidateNameForm(FormValidationAction):
    def name(self):
        return "validate_name_form"

    def validate_cust_name(self, slot_value, dispatcher, tracker, domain):
        return {"cust_name": slot_value}


    
