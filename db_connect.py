from pymongo.mongo_client import MongoClient

CONNECTION_STRING = ("mongodb+srv://top180802:PZSjSgsllE4zuV2L@cluster0.t9enqmi.mongodb.net/?retryWrites=true&w"
                     "=majority&appName=Cluster0")


def get_database():
    client = MongoClient(CONNECTION_STRING)

    return client['chatbot']


def store_training_data_in_mongodb(training_data):
    # Connect to MongoDB
    client = MongoClient(CONNECTION_STRING)
    db = client["chatbot"]
    collection = db["nlu"]

    # Insert each intent data into MongoDB
    for intent in training_data:
        data = {"intent": intent["intent"], "examples": intent["examples"]}
        collection.insert_one(data)


def store_stories_in_mongodb(stories):
    # Connect to MongoDB
    client = MongoClient(CONNECTION_STRING)
    db = client["chatbot"]
    collection = db["stories"]

    # Insert each story into MongoDB
    for story in stories:
        data = {"name": story["story"], "steps": story["steps"]}
        collection.insert_one(data)


def store_data_in_mongodb(data):
    # Connect to MongoDB
    client = MongoClient(CONNECTION_STRING)
    db = client["chatbot"]

    # Insert data into MongoDB
    for collection_name, documents in data.items():
        if documents:
            collection = db[collection_name]
            collection.insert_many(documents)

if __name__ == "__main__":
    dbname = get_database()