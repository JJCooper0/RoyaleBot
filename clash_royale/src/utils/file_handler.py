import json

def store_to_file(filename, data):
     with open(f"{filename}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)