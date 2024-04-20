import flask
import index
import re
import logging
@index.app.route('/api/v1/', methods=["GET"])
def get_index():
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)

def search_word(keyword):# ['hello', 'world']
    results = []
    for part in index.INDEXES:
        lines = part.split('\n')
        for line in lines:
            if len(line) == 0:
                continue
            word = line[0]
            idfk = line[1]
            data = []
            i = 4
            while i < len(line):
                doc_id = line[i-2]
                tfik = line[i-1]
                data.append((doc_id, tfik*idfk))
                i+=3
            results.append((word, data))
    return results

def load_stopwords(filepath):
    """Load stop words from stopwords.txt."""
    with open(filepath, 'r') as file:
        stopwords = set(file.read().split())
    return stopwords

def cleaning(text):
    """Clean text before parsing."""
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    text = text.casefold()
    terms = text.split()
    stopwords = load_stopwords('index_server/index/stopwords.txt')
    cleaned_terms = [term for term in terms if term not in stopwords]

    return cleaned_terms

@index.app.route('/api/v1/hits/', methods=["GET"])
def get_hit():
    query = flask.request.args.get('q')
    query = cleaning(query)
    results = search_word(query)
    print(results)
    print("Cleaned Queryssss:", query)
    context = {
        "doc_id": len(query),
        "score": "/api/v1/"
    }
    # for result in results:
    #     context.
    
    return flask.jsonify(**context)