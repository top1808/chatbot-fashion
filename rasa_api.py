import json
import requests
def parseModel(data):
    payload = json.dumps({"text": data["message"], "message_id": data["user"]})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.request("POST", url="http://localhost:5005/model/parse", headers=headers,
                                data=payload)
    return response.json()

def getConversation(id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.request("GET", url=f"http://localhost:5005/conversations/{id}/tracker", headers=headers)
    return response.json()
