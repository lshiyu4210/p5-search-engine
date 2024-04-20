"""
Search Server index (main) view.

URLs include:
/
"""
from flask import render_template, request
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from search.config import SEARCH_INDEX_SEGMENT_API_URLS 
import search

def get_hits(server_url, query_params):
    """Define a function to get hits from a server."""
    response = requests.get(server_url, params=query_params)
    response.raise_for_status()
    return response.json()['hits']

def get_top_10_results(query):
    query_params = {'q': query}
    with ThreadPoolExecutor(max_workers=len(SEARCH_INDEX_SEGMENT_API_URLS)) as executor:
        future_to_url = {
            executor.submit(get_hits, url, query_params): url 
            for url in SEARCH_INDEX_SEGMENT_API_URLS
        }
        
        all_hits = []
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                all_hits.extend(data)
            except Exception as exc:
                print(f'{url} generated an exception: {exc}')
    
    top_hits = sorted(all_hits, key=lambda x: x['score'], reverse=True)[:10]
    return top_hits

@search.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""
    query = request.args.get('q', '')
    weight = request.args.get('w', 0.5)
    if query:  # Only perform the search if there is a query
        top_hits = get_top_10_results(query)
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

        # Use the results to render the template
        return render_template('index.html', query=query, weight=weight, websites=websites)
    else:
        return render_template('index.html', query='', weight=weight, no_results=False, websites=[])
