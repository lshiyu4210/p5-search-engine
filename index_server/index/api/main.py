import flask
import index
import re
import collections
app = flask.Flask(__name__)

@index.app.route('/indexes/', methods=["GET"])
def show_indexes():
    return flask.jsonify(index.INDEXESx)

@index.app.route('/api/v1/', methods=["GET"])
def get_index():
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)

def search_word(keyword):# ['hello', 'world']  
    data = []
    print("size of index:", len(index.INDEXES))
    for part in index.INDEXES:
        lines = part.split('\n')
        for line in lines:
            entries = line.split()
            if len(entries) == 0:
                continue
            word = entries[0]
            if word == keyword:
                idf = float(entries[1])
                
                i = 4
                while i < len(entries):
                    doc_id = entries[i-2]
                    tf = int(entries[i-1])
                    data.append({"docid": doc_id,
                                 "tf": tf,
                                 "idf": idf})
                    i+=3
    return data

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

# def find_same_file(all_summaries):

        
@index.app.route('/api/v1/hits/', methods=["GET"])
def get_hit():
    query = flask.request.args.get('q')
    weight = flask.request.args.get('w', '0.5')
    query = cleaning(query)
    summary = []
    for q in query:
        print(q) 
        summary.append(search_word(q))
    if not summary:
        return flask.jsonify(hits=[])
    # if len(query) != 1:
    #     summary = find_same_file(summary)
    print(summary)
    context = {
        "hits": summary
    }
    return flask.jsonify(**context)