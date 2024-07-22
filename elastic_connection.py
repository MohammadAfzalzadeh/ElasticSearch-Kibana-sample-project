from elasticsearch import Elasticsearch

index_name = 'articles'

es = Elasticsearch(
    "https://localhost:9200",
    verify_certs=False,
    ca_certs="/path/to/ca.crt",
    api_key="Skc4Sm9wQUJPX3NLS1N3NldMU0Y6N0NkNEQ3anpTY21aQVkzdW91TVFMdw=="
)

def run_elastic_query(query): 
    response = es.search(index=index_name, body=query)
    hits = response['hits']['hits']
    return [hit['_source'] for hit in hits]