"""
Search Server index (main) view.

URLs include:
/
"""
from flask import render_template, request
import threading
import requests
from heapq import merge
import search

def fetch_hits(url, query_params, result_list):
    try:
        response = requests.get(url, params=query_params)
        response.raise_for_status()
        result_list.extend(response.json()['hits'])  # Use extend instead of append
    except requests.RequestException as e:
        print(f"Error fetching results from {url}: {e}")

def get_top_10_results(query):
    query_params = {'q': query}
    threads = []
    results = [[] for _ in range(len(search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]))]  # A list of lists to store results for each thread

    # Start a new thread for each index server URL
    for i, url in enumerate(search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]):
        thread = threading.Thread(target=fetch_hits, args=(url, query_params, results[i]))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Now, merge all results and sort them using heapq.merge
    all_sorted_hits = list(merge(*results, key=lambda x: x['score'], reverse=True))
    for r in results:
        print(r)

    # Return the top 10 hits
    return all_sorted_hits[:10]

@search.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""
    query = request.args.get('q', '')
    weight = request.args.get('w', 0.5)
    if query:  # Only perform the search if there is a query
        top_hits = get_top_10_results(query)
        # print(top_hits)
        # top_hits = [
        #     {"docid": 3929595},
        #     {"docid": 1210255},
        #     {"docid": 5529388},
        #     {"docid": 967365},
        #     {"docid": 7717709}
        # ]
        if not top_hits:
            return render_template('index.html', query=query, weight=weight, no_results=True)

        # Retrieve website details from the database
        connection = search.model.get_db()
        placeholders = ', '.join('?' for unused in top_hits)
        query_string = f'SELECT docid, title, summary, url FROM documents WHERE docid IN ({placeholders})'
        cur = connection.execute(query_string, [hit['docid'] for hit in top_hits])
        websites = cur.fetchall()
        for w in websites:
            print(w['title'])

        # Use the results to render the template
        return render_template('index.html', query=query, weight=weight, websites=websites)
    else:
        return render_template('index.html', query='', weight=weight, no_results=False, websites=[])
