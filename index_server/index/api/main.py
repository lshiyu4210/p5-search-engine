import flask
import index
import re
from functools import reduce
from index.api.config import INDICES, PAGERANK, STOPWORDS

app = flask.Flask(__name__)

@index.app.route('/api/v1/', methods=["GET"])
def get_index():
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)

def common_words(keyword):
    keyword_dicts = [INDICES[word] for word in keyword if word in INDICES]
    if not keyword_dicts:
        return set()
    common_docid = reduce(set.intersection, (set(d.keys()) for d in keyword_dicts))
    common_docid.discard('idfk')
    return common_docid
    

def cleaning(text):
    """Clean text before parsing."""
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    text = text.casefold()
    terms = text.split()
    cleaned_terms = [term for term in terms if term not in STOPWORDS]

    return cleaned_terms

        
@index.app.route('/api/v1/hits/', methods=["GET"])
def get_hit():
    query = flask.request.args.get('q', '')
    weight = flask.request.args.get('w', '0.5')

    query = cleaning(query)
    common_docid = common_words(query)
    context = {
        "hits": list(common_docid)
    }
    
    return flask.jsonify(**context)