import flask
import index
import re
from functools import reduce
from collections import Counter
import math
from index.api.config import INDICES, PAGERANK
import index.api.config as cfg

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
    for word in keyword:
        print(word, INDICES[word])
    if not keyword_dicts:
        return set()
    common_docid = reduce(set.intersection, (set(d.keys()) for d in keyword_dicts))
    common_docid.discard('idfk')
    return common_docid
    
def page_rank(weight, terms, term_frequencies, docid):
    """Calculate page rank for each docid."""
    # tfqk * idfk
    q = [term_frequencies[word] * INDICES[word]['idfk'] for word in terms if word in INDICES]
    # tfik * idfk
    d = [INDICES[word][docid][0] * INDICES[word]['idfk'] for word in terms if word in INDICES]
    dot_product = sum(x * y for x, y in zip(q, d))
    norm_q = math.sqrt(sum(x**2 for x in q))
    norm_d = math.sqrt(INDICES[terms[0]][docid][1])
    tf_idf = dot_product / (norm_q * norm_d)

    score = weight * PAGERANK[docid] + (1 - weight) * tf_idf
    return score


def cleaning(text):
    """Clean text before parsing."""
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    text = text.casefold()
    terms = text.split()
    cleaned_terms = [term for term in terms if term not in cfg.STOPWORDS]
    # print(cleaned_terms)
    # print(cfg.STOPWORDS)
    return cleaned_terms

        
@index.app.route('/api/v1/hits/', methods=["GET"])
def get_hit():
    query = flask.request.args.get('q', '')
    weight = flask.request.args.get('w', '0.5')

    # print(cfg.STOPWORDS)
    terms = cleaning(query)
    print(terms)
    for term in terms:
        if term not in INDICES:
            print(f"The word '{term}' is not in INDICES.")
            context = {
                "hits": []
            }
            return flask.jsonify(**context)

    term_frequencies = Counter(terms)
    common_docid = common_words(terms)
    hits = []
    for i in common_docid:
        temp_dict = {}
        temp_dict['docid'] = i
        temp_dict['score'] = page_rank(float(weight), terms, term_frequencies, i)
        hits.append(temp_dict)
    sorted_hits = sorted(hits, key=lambda x: x['score'], reverse=True)
    context = {
        "hits": sorted_hits
    }
    
    return flask.jsonify(**context)