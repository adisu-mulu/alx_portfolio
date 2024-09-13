"""This module serves as the application server"""
import urllib.request
import urllib.parse
import xmltodict
import json
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)
@app.route('/submit_comment', methods=['POST'])
def submit_form():
    """Method allows to submit comments"""
    message = request.form['message']
    return jsonify({'status': 'success', 'message': message})


def rank_papers(query, title_abstract):
    """Method ranks the papers fetched either by title or abstract"""
    # Combine the search query and the paper titles into one list
    documents = [query] + title_abstract
    # Use TF-IDF to vectorize the documents (ignoring common stop words)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    # Calculate cosine similarity between the query and the paper titles
    cosine_sim = cosine_similarity(tfidf_matrix[0:1],
                                   tfidf_matrix[1:]).flatten()
    # Rank papers based on similarity score (higher is more similar)
    rankings = sorted(enumerate(cosine_sim), key=lambda x: x[1], reverse=True)
    return rankings


@app.route('/search_by_title', methods=['POST'], strict_slashes=False)
def search_by_title():
    """Method fetches papers by their title"""
    message = request.form['search_query']
    base_url = 'http://export.arxiv.org/api/query?'
    params = {
         'search_query': f'all:{message}',
         'start': '0',
         'max_results': '15'
     }

    # Encode the parameters into the URL query string
    query_string = urllib.parse.urlencode(params)
    url = base_url + query_string

    # Open the URL and read the data
    response = urllib.request.urlopen(url)
    xml_data = response.read().decode('utf-8')

    # Convert XML to a dictionary
    data_dict = xmltodict.parse(xml_data)
    data_dict['search_by'] = 'Title'

    # Extract paper titles from the response
    papers = data_dict['feed']['entry']
    paper_titles = [paper['title'] for paper in papers]

    # Rank the papers based on similarity to the search query
    rankings = rank_papers(message, paper_titles)

    # Create a sorted list of papers based on the rankings
    ranked_papers = [papers[index] for index, score in rankings]
    # Replace the original list of papers with the ranked papers
    data_dict['feed']['entry'] = ranked_papers
    # Convert the combined data to JSON
    json_data = json.dumps(data_dict, indent=2)
    return json_data


@app.route('/search_by_abstract', methods=['POST'], strict_slashes=False)
def search_by_abstract():
    """Method fetches papers by their abstract"""
    message = request.form['search_query']  # Retrieve the search query
    base_url = 'http://export.arxiv.org/api/query?'
    params = {
        'search_query': f'abs:{message}',  # 'abs' for abstract search
        'start': '0',
        'max_results': '5'
    }

    # Encode the parameters into the URL query string
    query_string = urllib.parse.urlencode(params)
    url = base_url + query_string

    # Open the URL and read the data
    response = urllib.request.urlopen(url)
    xml_data = response.read().decode('utf-8')

    # Convert XML to a dictionary
    data_dict = xmltodict.parse(xml_data)
    data_dict['search_by'] = 'Abstract'  # Indicate search was by abstract

    # Extract paper abstracts from the response
    papers = data_dict['feed']['entry']
    paper_abstracts = [paper['summary'] for paper in papers]

    # Rank the papers based on similarity to the search query (abstract)
    rankings = rank_papers(message, paper_abstracts)

    # Create a sorted list of papers based on the rankings
    ranked_papers = [papers[index] for index, score in rankings]

    # Replace the original list of papers with the ranked papers
    data_dict['feed']['entry'] = ranked_papers
    # Convert dictionary to JSON
    json_data = json.dumps(data_dict, indent=2)
    return json_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
