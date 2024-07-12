
from db_connect import get_database
from bson import json_util

from utils.functionHelper import json_to_yaml

dbname = get_database()

if __name__ == "__main__":
    intents = dbname["intents"].find()
    intents_serializable = [json_util.loads(json_util.dumps(intent)) for intent in intents]
    json_to_yaml("test.yml", intents_serializable)