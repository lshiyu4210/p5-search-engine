import index.api.config as cfg

def load_index():
    """Load data into memory."""
    # global INDEXES, PAGERANK, STOPWORDS
    for i in range(3):
        file_path = f'index_server/index/inverted_index/inverted_index_{i}.txt'
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    main_key = parts[0]
                    # Initialize the main key if not already initialized
                    if main_key not in cfg.INDEXES:
                        cfg.INDEXES[main_key] = {}
                    # Assign the 'idfk' value
                    cfg.INDEXES[main_key]['idfk'] = float(parts[1])
                    # Iterate over the remaining parts of the line in steps of 3
                    for j in range(2, len(parts), 3):
                        sub_key = int(parts[j])  # Convert sub_key to integer
                        sub_value_1 = int(parts[j+1])
                        sub_value_2 = float(parts[j+2])
                        cfg.INDEXES[main_key][sub_key] = [sub_value_1, sub_value_2]
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    
    #load pagerank file
    pagerank_path = 'index_server/index/pagerank.out'
    with open(pagerank_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            page_id = int(parts[0])
            page_rank_score = float(parts[1])
            cfg.PAGERANK[page_id] = page_rank_score
    
    # Load stopwords file
    stopword_path = 'index_server/index/stopwords.txt'
    with open(stopword_path, 'r') as f:
        cfg.STOPWORDS = f.read().splitlines()
    
    print("Inverted Indexes, PageRank, and Stopwords have been loaded into memory.")