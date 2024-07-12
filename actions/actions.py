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
        dispatcher.utter_message(text=f"Chúng tôi đang có những chương trình khuyến mãi như {get_all_name_discount_programs()}. Bạn có thể tham khảo những sản phẩm giảm giá của những chương trình khuyến mãi này.")
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
        products = get_products_buy_name(item_type)
        print("item_type: ", item_type)
        if products:
            dispatcher.utter_message(text=f"Đây là 1 số loại {item_type} thích hợp để bạn chọn: {products}")
        else:
            dispatcher.utter_message(text=f"Xin lỗi chúng tôi không có sản phẩm này.")
        return []

class ActionCheckSize(Action):
    def name(self):
        return "action_check_size"

    def run(self, dispatcher, tracker, domain):
        cust_height = tracker.get_slot("cust_height")
        cust_weight = tracker.get_slot("cust_weight")
        item_type = tracker.get_slot("item_type")
        print("item_type: ", item_type)
        if cust_height:
            get_size = chose_size_from_height(cust_height)
            if get_size:
                dispatcher.utter_message(text=f"Bạn cao {cust_height} và nặng {cust_weight} thì nên mặc {item_type} size {get_size}.")
                dispatcher.utter_custom_message({'text': "image", 'class': "image", "url": "https://scontent.fsgn2-8.fna.fbcdn.net/v/t39.30808-6/450071881_1018050573026378_950725759138483731_n.jpg?_nc_cat=1&ccb=1-7&_nc_sid=127cfc&_nc_eui2=AeG-1vT2ahSlG0kF5wSTtXHJ9A5e7cgPL_H0Dl7tyA8v8WOPu74XiL_y0OI49ccmHov0lj-IxXL1FbI_5vOllGGW&_nc_ohc=IiDWflOtuSMQ7kNvgHQuALA&_nc_ht=scontent.fsgn2-8.fna&oh=00_AYAtbcsN1STTRRy1tcPXLphE5RlXUJgKiomS15l3nJdlWw&oe=6693509A"})
            else:
                dispatcher.utter_message(text=f"Xin lỗi chúng tôi không có size này. Vui lòng liên hệ với chúng tôi để đặt riêng.")
        else:
            dispatcher.utter_message(text=f"Tôi không biết")
        return []
    
class ActionCheckShoesSize(Action):
    def name(self):
        return "action_check_shoes_size"

    def run(self, dispatcher, tracker, domain):
        foot_size = tracker.get_slot("foot_size")
        print("foot_size", foot_size)
        if foot_size:
            get_size = chose_shoes_size_from_foot_size(foot_size)
            dispatcher.utter_message(text=f"Chân bạn dài {foot_size} thì nên đi size {get_size}.")
        else:
            dispatcher.utter_message(text=f"Tôi không biết")
        return []
    
class ValidateSizeForm(FormValidationAction):
    def name(self):
        return "validate_size_form"

    def validate_cust_height(self, slot_value, dispatcher, tracker, domain):
        return {"cust_height": slot_value}
    
    def validate_cust_weight(self, slot_value, dispatcher, tracker, domain):
        return {"cust_weight": slot_value}
    
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


    
