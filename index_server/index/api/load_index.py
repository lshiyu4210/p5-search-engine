
import index

# index_server/index/api.py
INDEXES, PAGERANK, STOPWORDS = None, {}, []

def load_index():
    """Load data into memory."""
    global INDEXES, PAGERANK, STOPWORDS

    #load inverted index file
    inverted_indexes = []
    for i in range(3):
        file_path = f'index_server/index/inverted_index/inverted_index_0000{i}.txt'
        with open(file_path, 'r') as f:
                inverted_indexes.append(f.read())
    
    #load pagerank file
    pagerank_path = 'index_server/index/pagerank.out'
    with open(pagerank_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            page_id = int(parts[0])
            page_rank_score = float(parts[1])
            PAGERANK[page_id] = page_rank_score
    
    # Load stopwords file
    stopword_path = 'index_server/index/stopwords.txt'
    with open(stopword_path, 'r') as f:
        STOPWORDS = f.read().splitlines()
    
    INDEXES = inverted_indexes
    print("Inverted Indexes, PageRank, and Stopwords have been loaded into memory.")