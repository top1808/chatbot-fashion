# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import Any, Dict, List, Text
from typing import Text
from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted, ConversationPaused
from rasa_sdk.executor import CollectingDispatcher

from utils.functionHelper import chose_size_from_height


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

class CheckSize(Action):
    def name(self):
        return "action_check_size"

    def run(self, dispatcher, tracker, domain):
        cust_height = tracker.get_slot("cust_height")
        cust_weight = tracker.get_slot("cust_weight")
        item_type = tracker.get_slot("item_type")
        if cust_height:
            get_size = chose_size_from_height(cust_height)
            dispatcher.utter_message(text=f"Bạn cao {cust_height} và nặng {cust_weight} thì nên mặc {item_type} size {get_size}.")
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
    
class ValidateNameForm(FormValidationAction):
    def name(self):
        return "validate_name_form"

    def validate_cust_name(self, slot_value, dispatcher, tracker, domain):
        return {"cust_name": slot_value}


    
