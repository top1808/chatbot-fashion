import json
import re
import requests
from bson import ObjectId, json_util
from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

from db_connect import get_database
from rasa_api import parseModel, getConversation
from utils.constants import ITEM_TYPE

dbname = get_database()
collection_name = dbname["intents"]

app = Flask(__name__)
cors = CORS(app, resources={r"/v3/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'application/json'

def replace_match(match):
    return f"[{match.group()}](item_type)"

@app.route("/v3/chatbot", methods=["POST"])
def chat():
    request_data = request.get_json()

    payload = json.dumps({"sender": request_data["user"], "message": request_data["message"]})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.request("POST", url="http://localhost:5005/webhooks/rest/webhook", headers=headers,
                                data=payload)
    response = response.json()

    if (len(response) == 0):
        return json.dumps({"data": "Có lỗi xảy ra."})
    conversation = getConversation(response[0]["recipient_id"])
    ranking = parseModel(request_data)["intent_ranking"]
    chat_collection = dbname["chats"]
    resp = []
    for item in response:
        if 'image' in item and item['image']:
            resp.append(item['image'])
        if 'attachment' in item and item['attachment']:
            resp.append(item['attachment'])
        if 'text' in item and item['text']:
            resp.append(item['text'])
    result = resp

    if ranking[0]["name"] == "nlu_fallback":
        intent_collection = collection_name.find_one({"intent": ranking[1]["name"]})
        if intent_collection:
            pattern = r'\b(' + '|'.join(map(re.escape, ITEM_TYPE)) + r')\b'
            new_text = re.sub(pattern, replace_match, request_data["message"])
            intent_collection["patterns"].append(new_text)
            collection_name.update_one({"intent": intent_collection["intent"]}, {"$set": intent_collection})

    chat_collection.insert_one({
        "user": request_data["message"],
        "bot": result[0] if len(result) > 0 else "",
        "conversation": conversation,
        "ranking": ranking,
        "date_time": datetime.datetime.now()
    })
    return json.dumps({"data": result})


@app.route("/v3/intents/get")
def getIntents():
    intents = collection_name.find()
    intents_serializable = [json_util.loads(json_util.dumps(intent)) for intent in intents]

    for intent in intents_serializable:
        intent['_id'] = str(intent['_id'])
    return jsonify({"data": intents_serializable})


@app.route("/v3/intents/get-by-id/<id>")
def getIntentById(id):
    intent = collection_name.find_one({'_id': ObjectId(id)})
    intent['_id'] = str(intent['_id'])
    return jsonify({"data": intent})


@app.route("/v3/intents/add", methods=["POST"])
def addIntents():
    request_data = request.get_json()
    collection_name.insert_one({
        "intent": request_data["intent"],
        "patterns": request_data["patterns"],
    })
    return jsonify({"success": request_data})


@app.route("/v3/intents/edit/<id>", methods=["PUT"])
def editIntents(id):
    try:
        request_data = request.get_json()
        collection_name.update_one({'_id': ObjectId(id)}, {"$set": {
            "intent": request_data["intent"],
            "patterns": request_data["patterns"],
        }})
        return jsonify({"success": True, "message": "Edit intents success."})
    except:
        return jsonify({"success": False, "message": "Edit intents failed."})


if __name__ == "__main__":
    app.run(debug=True)