import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from elastic_connection import run_elastic_query 


# Define the query
query = {
    "query": {
        "match": {
            "Title": "ethereum"
        }
    }
}


res_serializable = run_elastic_query(query)

# Store the result in a file
with open(f'{os.path.dirname(__file__)}/query_result.json', 'w') as f:
    json.dump(res_serializable, f, indent=4)

print("Query results have been stored in query_result.json")
