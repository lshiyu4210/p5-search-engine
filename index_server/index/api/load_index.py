import index
# index_server/index/api.py
INDEXES, PAGERANK, STOPWORDS = [], {}, []
# global INDEXESx
def load_index():
    """Load data into memory."""
    # global INDEXES, PAGERANK, STOPWORDS
    #load inverted index file
    inverted_indexes = []
    for i in range(3):
        file_path = f'index_server/index/inverted_index/inverted_index_0000{i}.txt'
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                inverted_indexes.append(content)
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
   
    index.INDEXES = inverted_indexes
    index.INDEXESx = ['index1', 'index2', 'index3']
    print(index.INDEXESx)
    
    
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
    
    
    print("Inverted Indexes, PageRank, and Stopwords have been loaded into memory.")