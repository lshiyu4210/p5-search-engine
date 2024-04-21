"""Index server API."""
import re
import copy
import flask
import index


@index.app.route('/api/v1/', methods=["GET"])
def get_index():
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


def cleaning(query):
    """clean up query words"""
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.casefold()
    query = query.strip().split()
    query = [word for word in query if word not in index.stopwords_set]
    return query


def make_query_dict(query):
    """{term: value}"""
    query_dict = {}
    for term in query:
        if term not in query_dict:
            query_dict[term] = 1
        else:
            query_dict[term] += 1
    return query_dict

def make_doc_id_set(query):
    """pick overlapping term doc_id set"""
    tempList = []
    tempSet = set()
    for term, _ in query.items():
        term_dict = index.index_list[term]
        for doc_id, _ in term_dict.items():
            if doc_id != "idf":
                tempSet.add(doc_id)
        tempList.append(copy.deepcopy(tempSet))
        tempSet.clear()

    result_set = tempList[0]
    for single_set in tempList[1:]:
        result_set = result_set.intersection(single_set)
    return result_set

def create_document_vector(doc_id_set, doc_vector_dict, query):
    for doc_id in doc_id_set:
        doc_vector = []
        for term, _ in query.items():
            tf_val = index.index_list[term][doc_id]
            entry = float(index.index_list[term]['idf']) * float(tf_val)
            doc_vector.append(entry)
        doc_vector_dict[doc_id] = copy.deepcopy(doc_vector)
    return doc_vector_dict

def calc_tfidf(doc_score_dict, query_vector, doc_vector_dict):
    for doc_id, doc_vector in doc_vector_dict.items():
        dot_product = 0
        for ele1, ele2 in zip(query_vector, doc_vector):
            dot_product += ele1 * ele2
        doc_score_dict[doc_id] = dot_product
    return doc_score_dict

def calc_with_weight(doc_score_dict, q_norm, weight):
    for doc_id, score in doc_score_dict.items():
        d_norm = float(index.doc_n_factor[doc_id]) ** (1 / 2)
        tfidf = score / (q_norm * d_norm)
        score = weight * \
            float(index.pagerank_list[doc_id]) + (1 - weight) * tfidf
        doc_score_dict[doc_id] = score
    return doc_score_dict

@index.app.route("/api/v1/hits/", methods=["GET"])
def get_hit():
    weight = float(flask.request.args.get('w', '0.5'))
    query = flask.request.args.get('q')
    #clean up 
    query = cleaning(query)
    
    #no word
    if len(query) == 0:
        context = {"hits": []}
        return flask.jsonify(**context)

    #calculate query vector
    query = make_query_dict(query)
    query_vector = []
    q_norm = 0
    
    for term, query_tf in query.items():
        if term not in index.index_list:
            context = {"hits": []}
            return flask.jsonify(**context)

        num = query_tf * float(index.index_list[term]['idf'])
        q_norm += num ** 2
        query_vector.append(num)

    #calculate documnet vector
    doc_id_set = make_doc_id_set(query)
    doc_vector_dict = {}
    doc_id_set = create_document_vector(doc_id_set, doc_vector_dict, query)
    
    #calculate tf-idf
    doc_score_dict = {}
    doc_score_dict = calc_tfidf(doc_score_dict, query_vector, doc_vector_dict)

    #add weights to the score
    q_norm = q_norm ** (1 / 2)
    doc_score_dict = calc_with_weight(doc_score_dict, q_norm, weight)
    
    hits = []
    doc_score_dict = sorted(
        doc_score_dict.items(),
        key=lambda x: x[1],
        reverse=True)
    for doc_id, score in doc_score_dict:
        temp_dict = {}
        temp_dict["docid"] = int(doc_id)
        temp_dict["score"] = score
        hits.append(temp_dict)

    context = {}
    context["hits"] = hits

    return flask.jsonify(**context)