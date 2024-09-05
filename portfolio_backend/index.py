import urllib.request
import urllib.parse
import xmltodict
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/submit_comment', methods=['POST'])
def submit_form():
    message = request.form['message']
    
    return jsonify({'status': 'success', 'message': message})

@app.route('/search_by_title', methods=['POST'], strict_slashes=False)
def search_by_title():
    message = request.form['search_query']
    base_url = 'http://export.arxiv.org/api/query?'
    params = {
         'search_query': f'all:{message}',
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
    data_dict['search_by'] ='Title'
     # Convert dictionary to JSON
    json_data = json.dumps(data_dict, indent=2)
     
    return json_data
   # return jsonify({'search_by': 'Title', 'message': message, 'author': "Adisu", 'area': "ML", 'year': "1990"})

@app.route('/search_by_abstract', methods=['POST'], strict_slashes=False)
def search_by_abstract():
    message = request.form['search_query']
    return jsonify({'search_by': 'Abstract', 'message': message, 'author': "Adisu", 'area': "ML", 'year': "1990"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
                                    
