import sys
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, render_template

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from elastic_connection import run_elastic_query



def get_all_data():
    query = {
        "query": {
            "match_all": {}
        }
    }
    return run_elastic_query(query)

def get_specific_data(doi):
    query = {
        "query": {
            "match": {
                "DOI": doi
            }
        }
    }
    return run_elastic_query(query)
    

def calculate_tfidf(texts):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix

def calculate_similarity_and_scores(specific_title, specific_abstract, specific_keywords, all_titles, all_abstract, all_keywords , top_n):

    # Calculate TF-IDF matrices
    tfidf_matrix_titles = calculate_tfidf(all_titles)
    tfidf_matrix_abstract = calculate_tfidf(all_abstract)
    tfidf_matrix_keywords = calculate_tfidf(all_keywords)

    # Get indices
    specific_index_title = all_titles.index(specific_title)
    specific_index_abstract = all_abstract.index(specific_abstract)
    specific_index_keywords = all_keywords.index(specific_keywords)

    # Calculate cosine similarities
    cosine_sim_titles = cosine_similarity(tfidf_matrix_titles[specific_index_title], tfidf_matrix_titles).flatten()
    cosine_sim_abstract = cosine_similarity(tfidf_matrix_abstract[specific_index_abstract], tfidf_matrix_abstract).flatten()
    cosine_sim_keywords = cosine_similarity(tfidf_matrix_keywords[specific_index_keywords], tfidf_matrix_keywords).flatten()

    # Compute results
    final_scores = {}
    for j, title in enumerate(all_titles):
        if j == specific_index_title:
            continue
        score = (cosine_sim_titles[j] + cosine_sim_abstract[j] + cosine_sim_keywords[j]) / 3
        final_scores[title] = score

    # Sort final scores
    sorted_final_scores = dict(sorted(final_scores.items(), key=lambda item: item[1], reverse=True))
    
    return dict(list(sorted_final_scores.items())[:top_n])
     

app = Flask(__name__)

@app.route('/', methods=['GET'])
def indx():
    return render_template('index.html')

@app.route('/RS', methods=['POST'])
def RS():
    doi = request.form['doi']
    top_n = int(request.form['top_n'])
    

    specific_data = get_specific_data(doi)
    
    if not specific_data:
        return "DOI not found", 404
    
    specific_title = specific_data[0]['Title']
    specific_abstract = specific_data[0]['abstract']
    specific_keywords = ' '.join(specific_data[0]['Author Keywords'])

    print(specific_title , specific_keywords , specific_abstract)

    data = get_all_data()

    all_titles = [item['Title'] for item in data]
    all_abstract = [item['abstract'] for item in data]
    all_keywords = []
    for item in data : 
        keywords_sim = item['Author Keywords'] or []
        all_keywords.append( ' '.join(keywords_sim))


    final_scores_top = calculate_similarity_and_scores(specific_title, specific_abstract, specific_keywords, all_titles, all_abstract, all_keywords , top_n)
    
    return render_template('results.html', specific_DOI = doi , specific_title=specific_title,  final_scores=final_scores_top)

if __name__ == '__main__':
    app.run(debug=True , port=3001)
