import os
import json

def replace_text_in_nested_json(obj, search_text, replacement_text):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = replace_text_in_nested_json(value, search_text, replacement_text)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            obj[i] = replace_text_in_nested_json(value, search_text, replacement_text)
    elif isinstance(obj, str):
        return obj.replace(search_text, replacement_text)

    return obj

def replace_text_in_json_files(directory, search_text, replacement_text):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                data = json.load(file)

            data_modified = replace_text_in_nested_json(data, search_text, replacement_text)

            with open(filepath, "w") as file:
                json.dump(data_modified, file, indent=2)

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    search_text = "https://elk.finance/tokens/logos/"
    replacement_text = "https://raw.githubusercontent.com/elkfinance/tokens/main/logos/"

    replace_text_in_json_files(directory, search_text, replacement_text)
