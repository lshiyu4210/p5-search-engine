
import index
# index_server/index/api.py
def load_index():
    #loda inverted index file
    inverted_indexes = []
    for i in range(3):
        file_path = f'index_server/index/inverted_index/inverted_index_0000{i}.txt'
        with open(file_path, 'r') as f:
                inverted_indexes.append(f.read())
    
    #load pagerank file
    
    pagerank_path = 'index_server/index/pagerank.out'
    with open(pagerank_path, 'r') as f:
        pagerank_data = f.read()
    
    # Load stopwords file
    stopword_path = 'index_server/index/stopwords.txt'
    with open(stopword_path, 'r') as f:
        stopwords = f.read().splitlines()
    global INDEXES, PAGERANK, STOPWORDS
    INDEXES = inverted_indexes
    PAGERANK = pagerank_data
    STOPWORDS = stopwords
    print("Inverted Indexes, PageRank, and Stopwords have been loaded into memory.")