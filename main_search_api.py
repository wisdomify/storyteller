from storyteller.connectors import connect_to_es
from storyteller.elastic.searcher import Searcher
from storyteller.elastic.docs import Story
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

    
@app.route('/', methods=['GET'])
def check():
    if request.method == 'GET':
        return "connected"
    
@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        req = json.loads(request.data)
        wisdom = req['wisdom']
        index_name = ",".join(Story.all_indices())
        size = 10000
        with connect_to_es() as es:
            searcher = Searcher(es) 
            res = searcher(wisdom, index_name, size)
            
            parsed = [
                f"index: {hit['_index']}, highlight:{hit['highlight']['sents'][0]}"
                for hit in res['hits']['hits']
            ]
            return jsonify(parsed)
        
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)