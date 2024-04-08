import json
import requests
from bson import ObjectId, json_util
from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

from db_connect import get_database

dbname = get_database()
collection_name = dbname["intents"]

app = Flask(__name__)
cors = CORS(app, resources={r"/v3/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'application/json'


@app.route("/v3/chatbot", methods=["POST"])
def chat():
    request_data = request.get_json()
    payload = json.dumps({"sender": "Rasa", "message": request_data["message"]})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.request("POST", url="http://localhost:5005/webhooks/rest/webhook", headers=headers,
                                data=payload)
    response = response.json()
    chat_collection = dbname["chats"]
    resp = []
    for i in range(len(response)):
        try:
            resp.append(response[i]['text'])
        except:
            continue
    result = resp
    chat_collection.insert_one({
        "user": request_data["message"],
        "bot": result[0] if len(result) > 0 else "", 
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
        print(request_data)
        collection_name.update_one({'_id': ObjectId(id)}, {"$set": {
            "intent": request_data["intent"],
            "patterns": request_data["patterns"],
        }})
        return jsonify({"success": True, "message": "Edit intents success."})
    except:
        return jsonify({"success": False, "message": "Edit intents failed."})


if __name__ == "__main__":
    app.run(debug=True)