"""Load index."""
import index

stopwords_path = index.app.config["FILE_PATH"] / 'stopwords.txt'
pagerank_path = index.app.config["FILE_PATH"] / 'pagerank.out'
index_path = index.app.config["INDEX_DICT_PATH"]


def load_index():
    """Load the index file into memory."""
    
    #  Load the stopword files into memory 
    with open(stopwords_path, 'r', encoding='utf-8') as file:
        index.stopwords_set = set(file.read().split())

    temp_dict = {}
    #  load the pagerank file into memory
    with open(pagerank_path, 'r', encoding='utf-8') as file:
        index.pagerank_list = [line.strip() for line in file.readlines()]

    #  load the inverted index
    with open(index_path, 'r', encoding='utf-8') as file:
        index.index_list = [line.strip() for line in file.readlines()]
        
    for line in index.pagerank_list:
        doc_id, pagerank = line.split(',')[0], line.split(',')[1]
        temp_dict[doc_id] = pagerank
    index.pagerank_list = temp_dict

    temp_dict = {}
    doc_n_factor = {}

    for line in index.index_list:
        entry = line.split()
        term = entry[0]
        idf = entry[1]
        temp_dict[term] = {'idf': idf}

        for i in range(2, len(entry), 3):
            doc_id = entry[i]
            term_freq = entry[i + 1]
            n_factor = entry[i + 2]
            doc_n_factor[doc_id] = n_factor
            temp_dict[term][doc_id] = term_freq

    index.index_list = temp_dict
    index.doc_n_factor = doc_n_factor
