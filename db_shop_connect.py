from bson import ObjectId, json_util
from pymongo.mongo_client import MongoClient
from thefuzz import process

CONNECTION_STRING = ("mongodb+srv://top1808:vGSlA80YSUPiFgSr@cluster0.7alxuod.mongodb.net/?retryWrites=true&w"
                     "=majority&appName=Cluster0")

def get_database():
    client = MongoClient(CONNECTION_STRING)

    return client['test']

def get_products_by_name(name = "", limit = 10):
    client = get_database()

    products = client["products"].find()
    products_names = [product["name"] for product in products]
    products = process.extract(name, products_names, limit=limit)

    products = [product for product in products if product[1] >= 50]
    products = [product[0] for product in products[:5]]
    new_products = []
    for product in products:
        new_product = client["products"].find_one({"name": product})
        new_products.append(new_product)

    products_serializable = [json_util.loads(json_util.dumps(product)) for product in new_products]

    for product in products_serializable:
        product['_id'] = str(product['_id'])
    return products_serializable

def get_products(limit = 5):
    client = get_database()
    products = client["products"].find().limit(limit)
    products_serializable = [json_util.loads(json_util.dumps(product)) for product in products]

    for product in products_serializable:
        product['_id'] = str(product['_id'])
    return products_serializable

def get_product_by_id(id):
    client = get_database()
    product = client["productdiscounts"].find_one({"_id": ObjectId(id)})
    product = client["products"].find_one({"_id": ObjectId(product["productCode"])})
    product['_id'] = str(product['_id'])
    return product
def get_categories(limit = 5):
    client = get_database()
    categories = client["categories"].find().limit(limit)
    categories_serializable = [json_util.loads(json_util.dumps(categories)) for categories in categories]

    for categories in categories_serializable:
        categories['_id'] = str(categories['_id'])
    return categories_serializable

def get_discount_programs(limit = 5):
    client = get_database()
    discount_programs = client["discountprograms"].find().limit(limit)
    discount_programs_serializable = [json_util.loads(json_util.dumps(discount_programs)) for discount_programs in discount_programs]

    for discount_program in discount_programs_serializable:
        discount_program['_id'] = str(discount_program['_id'])
    return discount_programs_serializable

def get_discountPrograms():
    client = get_database()
    discountPrograms = client["discountprograms"].find()
    discountPrograms_serializable = [json_util.loads(json_util.dumps(discountPrograms)) for discountPrograms in discountPrograms]

    for discountPrograms in discountPrograms_serializable:
        discountPrograms['_id'] = str(discountPrograms['_id'])
    return discountPrograms_serializable

def get_vouchers():
    client = get_database()
    vouchers = client["vouchers"].find()
    vouchers_serializable = [json_util.loads(json_util.dumps(vouchers)) for vouchers in vouchers]

    for vouchers in vouchers_serializable:
        vouchers['_id'] = str(vouchers['_id'])
    return vouchers_serializable