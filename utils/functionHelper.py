import os
from db_shop_connect import get_products, get_categories, get_products_by_name, get_discount_programs
import re
import json

size_data = [
    {
        "minHeight": 141,
        "maxHeight": 150,
        "size": "XS"
    },
    {
        "minHeight": 151,
        "maxHeight": 160,
        "size": "S"
    },
    {
        "minHeight": 161,
        "maxHeight": 170,
        "size": "M"
    },
    {
        "minHeight": 171,
        "maxHeight": 180,
        "size": "L"
    },
    {
        "minHeight": 181,
        "maxHeight": 190,
        "size": "XL"
    },
]

shoes_size_data = [
    {
        "foot_length": 22,
        "size": 35
    },
    {
        "foot_length": 22.5,
        "size": 36
    },
    {
        "foot_length": 23,
        "size": 37
    },
    {
        "foot_length": 23.5,
        "size": 38
    },
    {
        "foot_length": 24,
        "size": 38.5
    },
    {
        "foot_length": 24.5,
        "size": 39
    },
    {
        "foot_length": 25,
        "size": 40
    },
    {
        "foot_length": 26,
        "size": 41
    },
    {
        "foot_length": 27,
        "size": 42
    },
    {
        "foot_length": 27.5,
        "size": 43
    },
]


def convert_size_to_number(height):
    if height is None: return ""
    parts = height.split('m')
    if 'cm' not in height and len(parts) == 2:
        meters = parts[0]
        cms = parts[1].replace("cm", "")
        height_cm = float(meters) * 100 + (float(cms) if float(cms) > 10 else float(cms) * 10)
        return height_cm
    elif 'cm' in height:
        cms = height.replace("cm", "")
        return float(cms)
    else:
        return ""


def chose_size_from_height(height):
    convert_height = convert_size_to_number(height)
    for size_info in size_data:
        if size_info["minHeight"] <= convert_height <= size_info["maxHeight"]:
            return size_info["size"]
    return ""

def chose_shoes_size_from_foot_size(footsize):
    convert_size = convert_size_to_number(footsize)
    closest_size = None
    min_difference = float('inf')
    for shoe in shoes_size_data:
        difference = abs(shoe["foot_length"] - convert_size)
        if difference < min_difference:
            min_difference = difference
            closest_size = shoe["size"]
    
    return closest_size

def get_all_name_products():
    products = get_products()
    names = []
    for product in products:
        names.append(product["name"])
    
    return ", ".join(names)

def get_all_name_categories():
    categories = get_categories()
    names = []
    for category in categories:
        names.append(category["name"])
    
    return ", ".join(names)

def get_all_name_discount_programs():
    discount_programs = get_discount_programs()
    names = []
    for discount_program in discount_programs:
        names.append(discount_program["name"])
    
    return ", ".join(names)
def get_products_buy_name(name):
    if name == "":
        return ""
    products = get_products_by_name(name)
    names = []
    for product in products:
        names.append(product["name"])
    
    return ", ".join(names)

def readFileJson(json_file):
    data = ""
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
def json_to_yaml(yaml_file, json_data):
    if os.path.exists(yaml_file):
        os.remove(yaml_file)
    with open(yaml_file, 'w', encoding='utf-8') as file:
        file.write('')
    with open(yaml_file, 'r', encoding='utf-8') as file:
        yaml_content = file.read()
    yaml_content = """version: "3.1"\nnlu:\n""" + yaml_content

    name_data = readFileJson('vietnamese_name/name.json')["name"]
    name_intent = {
        "intent": "give_name",
        "patterns": [f"[{name}](cust_name)" for name in name_data]
    }
    json_data.append(name_intent)
    # print(json_data)
    for item in json_data:
        intent = item['intent']
        new_examples = item['patterns']

        intent_pattern = rf"- intent: {intent}\n  examples: \|([\s\S]*?)(?=\n- intent:|\Z)"
        intent_match = re.search(intent_pattern, yaml_content, re.DOTALL)
        if intent_match:
            current_examples = intent_match.group(1).strip().split('\n')
            current_examples = [e.strip() for e in current_examples if e.strip()]
            for example in new_examples:
                temp = '- ' + example
                if temp not in current_examples:
                    current_examples.append(example)

            new_examples_str = '\n'.join([f"  {e}" if e.strip().startswith('- ') else f"  - {e}" for e in current_examples])
            
            updated_intent = f"- intent: {intent}\n  examples: |\n{new_examples_str}\n"
            yaml_content = re.sub(intent_pattern, updated_intent, yaml_content, flags=re.DOTALL)
        else:
            new_item = f"\n- intent: {intent}\n  examples: |\n" + \
                       '\n'.join([f"    - {e}" for e in new_examples]) + "\n"
            yaml_content = yaml_content.rstrip() + new_item

    yaml_content = yaml_content.rstrip() + "\n"

    with open(yaml_file, 'w', encoding='utf-8') as file:
        file.write(yaml_content)