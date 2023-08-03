import json
from function.dataProcessor import dataProcessing

if __name__ == "__main__":
    with open('./data/temp.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        dataProcessing(data)
