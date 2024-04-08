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


def convert_height_to_number(height):
    print("height: ", height)
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
    convert_height = convert_height_to_number(height)
    for size_info in size_data:
        if size_info["minHeight"] <= convert_height <= size_info["maxHeight"]:
            return size_info["size"]
    return ""
