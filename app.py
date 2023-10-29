from flask import Flask, request, jsonify
from constants import *

from haystack.document_stores import InMemoryDocumentStore
from haystack.utils import build_pipeline, add_example_data, print_answers, print_documents

app = Flask(__name__)
    
class semantic_search:
    def __init__(self):
        print(f"initializing semantic search algorithm{'.'*90}")

        document_store = InMemoryDocumentStore(use_bm25=True)
        add_example_data(document_store, patent_txt_folder_path)
        self.pipeline = build_pipeline(provider, API_KEY, document_store)

    def Search(self, param):
        print(f"seach begins{'.'*90}")
        # Ask a question on the data you just added.
        # result = pipeline.run(query="where the instruction is decoded and dispatched ")
        param  = " ".join(param) if isinstance(param, list) else param
        result = self.pipeline.run(query=param)
        file_names = []
        for r in result['documents']:
            print(r.content[:20], r.meta["name"], r.score, sep="\t")
            file_names.append(r.meta["name"].split(".", maxsplit=1)[0])
        return file_names
 
@app.route('/search', methods=['GET'])
def search():
    try:
        # Get parameters from the URL
        param = request.args.get('query')
        print(f"Query provided: {param}")
        result = ss_obj.Search(param)
        
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    ss_obj = semantic_search()
    app.run(debug=True)
