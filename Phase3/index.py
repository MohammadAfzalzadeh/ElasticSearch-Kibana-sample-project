import sys
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from elastic_connection import run_elastic_query , es

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search_articles():
    query_data = request.json
    query = {
        "query": {
            "bool": query_data
        }
    }

    articles = run_elastic_query(query)

    index_name = 'queryed_article'
    es.indices.delete(index=index_name, ignore=[400, 404])
    es.indices.create(index=index_name)

    for article in articles:
        es.index(index=index_name, document=article)
    
    
    return jsonify({"message": "Query executed and results indexed.", "results": articles})

if __name__ == '__main__':
    app.run(debug=True , port=3000)
