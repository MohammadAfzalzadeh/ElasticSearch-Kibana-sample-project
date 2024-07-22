# ElasticSearch & Kibana sample project

## Section Zero: Connecting to Elastic Search

The `elastic_connection.py` file in this project is used to connect to the Elasticsearch service. This file includes connection settings for Elasticsearch and a function to execute Elasticsearch queries. Here are brief explanations of each part of this file:

1. **Connecting to Elasticsearch:**
   In this section, a connection to Elasticsearch is established with the following specifications:
   - Address `https://localhost:9200` for connecting to the local Elasticsearch service.
   - `verify_certs=False` to disable SSL certificate verification.
   - `ca_certs="/path/to/ca.crt"` to specify the CA certificate file path (if needed).
   - `api_key` to use an API key for authentication.

2. **`run_elastic_query` function:**
   This function is used to execute a query in Elasticsearch and returns the results as a list of documents obtained from the search results.

This file is used as a separate module throughout the project to manage the connection to Elasticsearch and execute the required queries.

This first section of the project analyzes JSON data and sends it to Elasticsearch. The following code is executed in this section:

## Section One - Analyzing JSON Data and Sending to Elasticsearch

1. **Docker Instructions:**

Setting up Elasticsearch and Kibana with Docker:
   ```bash
   docker run --name es01 --rm -it --net elastic -p 9200:9200 -m 1GB docker.arvancloud.ir/elasticsearch:8.13.4

   docker run --name kib01 --rm --net elastic -p 5601:5601 docker.arvancloud.ir/kibana:8.13.4
   ```

2. **Data Processing Functions:**
   - `convert_votes_to_int(votes_str)`: A function that converts a string containing votes to an integer.
   - `process_json_file(file_path)`: This function opens a JSON file, analyzes the data, and converts the votes if possible.
   - `read_and_convert_votes(directory)`: This function reads all JSON files in a specified directory, prepares them for analysis, and sends them to Elasticsearch.

3. **Sending Data to Elasticsearch:**
   ```python
   directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
   articles = read_and_convert_votes(directory_path)

   for article in articles:
       es.index(index="articles", document=article)
   ```
   - In this section, all articles read from the JSON files are sent to Elasticsearch. This is done using the `es` object imported from the `elastic_connection.py` file.

### Section Two - Executing Queries in Elasticsearch and Saving Results

1. **Import and Path Settings:**

2. **Defining the Query:**
   ```python
   # Define the query
   query = {
       "query": {
           "match": {
               "Title": "ethereum"
           }
       }
   }
   ```
   - Here, a simple query is defined to search for the term "ethereum" in the "Title" field.

3. **Executing the Query and Saving Results:**

   - This section includes executing the query using the `run_elastic_query` function defined in the `elastic_connection.py` file.
   - The query results are saved in JSON format using the `json` library and stored in the `query_result.json` file.
   - A message is displayed indicating that the query results are saved in the `query_result.json` file.

This section of the project is designed to execute a query in Elasticsearch using a `elastic_connection.py` file to search for "ethereum" in the "Title" field and save the results in a JSON file.

[query-result](./Phase2/query_result.json)

The query was also executed using the Kibana tool:
![kibana Query](./Phase2/Kibana%20Search.png)

## Section Three: Complex Query
The JavaScript code in this section is used to define and send complex searches to Elasticsearch. This code provides the following functionalities to the user:

1. **Adding and Removing Search Groups:** The user can add or remove search groups using the "Add" and "Remove" buttons. This allows the user to define multiple and more complex searches for Elasticsearch.

2. **Selecting Boolean Operators:** Each search group has a logical operator like "AND", "OR", or "NOT" that the user can use to define various logical relationships between search conditions.

3. **Selecting Fields (Metadata):** The user can choose the desired field for the search from options like "abstract", "IEEE keywords", "DOI", and "Title". This selection allows the user to choose the most logical field for the desired information search.

4. **JSON Structure for Elasticsearch:** After collecting the necessary information, a JSON structure is created for sending to Elasticsearch. This structure includes "must", "should", and "must_not" conditions for use in an Elasticsearch query, formed based on the user's selections.

5. **Sending the Query to the Flask Server:** After the Elasticsearch query is fully formed, it is sent to the Flask server. The Flask server uses the relevant libraries to send the query to Elasticsearch and return the results.

This process allows the user to define more complex searches for Elasticsearch based on their needs and retrieve the expected results from the information retrieval system.

After receiving the user's query, it is added to another index to create Kibana dashboards for it:
- Dashboard for all data:
![main-dashboard](./Phase3/Dashboard%20images/Article%20Dashboard.png)
- Dashboard for the user's required data:
![selected-dashboard](./Phase3/Dashboard%20images/new%20Article%20Dashboard.png)

[exportedDashboard](./Phase3/exportedDashboard.ndjson)

Execution Results:
![](./Phase3/Run%20Images/frontPage.png)
![](./Phase3/Run%20Images/new%20Index%20with%20search.png)
![](./Phase3/Run%20Images/new%20index.png)

## Section Four: Information Retrieval System Based on TF-IDF and Cosine Similarity
Files and Sections:
1. elastic_connection.py
This file includes code for connecting to Elasticsearch and executing various queries.

run_elastic_query(query): A function to execute Elasticsearch queries and return results.
2. main.py
This file includes the main code for calculating TF-IDF, Cosine Similarity, and running the Flask server to display results to the user.

get_all_data(): Returns all data available in Elasticsearch.
get_specific_data(doi): Returns specific data based on the DOI.
calculate_tfidf(texts): Calculates TF-IDF for the texts.
calculate_similarity_and_scores(): Calculates similarity and final scores based on TF-IDF and Cosine Similarity.
3. Templates: index.html and results.html
These two HTML files include the templates for the website pages for entering the site and displaying results.

- Execution Results:

![](./Phase4/run%20Images/rs%20query.png)
![](./Phase4/run%20Images/result.png)