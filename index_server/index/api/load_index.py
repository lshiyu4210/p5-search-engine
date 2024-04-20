
# index_server/index/api.py
INDEXES, PAGERANK, STOPWORDS = [], {}, []
INDEXESx = []
def load_index():
    """Load data into memory."""
    global INDEXES, PAGERANK, STOPWORDS
    #load inverted index file
    inverted_indexes = []
    for i in range(3):
        file_path = f'index_server/index/inverted_index/inverted_index_0000{i}.txt'
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                if content:  # Check if file read returns something non-empty
                    inverted_indexes.append(content)
                    print(f"Loaded {file_path} successfully.")  # Diagnostic print
                else:
                    print(f"Warning: {file_path} is empty.")  # Diagnostic print
                    
                # inverted_indexes.append(file.read())
                # print("loaded corresponding files")
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    if not inverted_indexes:
        print("No index files loaded. Check the file paths and names.")
    else:
        print(f"Total files loaded: {len(inverted_indexes)}")
   
    INDEXES = inverted_indexes
    INDEXESx = ['index1', 'index2', 'index3']
    print(INDEXESx)
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