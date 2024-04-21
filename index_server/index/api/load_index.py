"""Load index."""
import index

stopwords_path = index.app.config["FILE_PATH"] / 'stopwords.txt'
PAGERANK_PATH = index.app.config["FILE_PATH"] / 'pagerank.out'
index_path = index.app.config["INDEX_DICT_PATH"]

def load_index():
    """load the index file into two part here, one is index_list(which is dict here)
        the other one is doc_N_factor, which stores the Normalization factor
    """
    with open(stopwords_path, 'r', encoding='utf-8') as file:
        index.stopwords_set = set(file.read().split())

    temp_dict = {}
    with open(PAGERANK_PATH, 'r', encoding='utf-8') as file:
        index.pagerank_list = [line.strip() for line in file.readlines()]
    for line in index.pagerank_list:
        doc_id, pagerank = line.split(',')[0], line.split(',')[1]
        temp_dict[doc_id] = pagerank
    index.pagerank_list = temp_dict

    temp_dict = {}
    doc_n_factor = {}
    with open(index_path, 'r', encoding='utf-8') as file:
        index.index_list = [line.strip() for line in file.readlines()]

    for line in index.index_list:
        line_list = line.split()
        term = line_list[0]
        term_idf = line_list[1]
        temp_dict[term] = {'idf': term_idf}

        for i in range(2, len(line_list), 3):
            doc_id, term_freq, n_factor = line_list[i], line_list[i +
                                                           1], line_list[i + 2]
            doc_n_factor[doc_id] = n_factor
            temp_dict[term][doc_id] = term_freq

    index.index_list = temp_dict
    index.doc_n_factor = doc_n_factor