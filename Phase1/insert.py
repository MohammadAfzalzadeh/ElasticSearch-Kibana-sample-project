import sys
import os
import json
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from elastic_connection import es 

def convert_votes_to_int(votes_str):
    match = re.search(r'\d+', votes_str)
    if match:
        return int(match.group())
    else:
        return None

def process_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
        try:
            data = json.load(json_file)
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")
            return None

def read_and_convert_votes(directory):
    json_data = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                processed_data = process_json_file(file_path)
                if processed_data:
                    json_data.append(processed_data)
    
    return json_data

directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
articles = read_and_convert_votes(directory_path)


for article in articles:
    es.index(index="articles", document=article)


# docker run --name kib01 --rm     --net elastic -p 5601:5601         docker.arvancloud.ir/kibana:8.13.4
# docker run --name es01  --rm -it --net elastic -p 9200:9200 -m 1GB  docker.arvancloud.ir/elasticsearch:8.13.4 
