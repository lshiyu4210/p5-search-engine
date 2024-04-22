"""
Search Server index (main) view.

URLs include:
/
"""
import threading
from heapq import merge
from flask import render_template, request
import requests
import search


def fetch_hits(url, query_params, result_list):
    """Fetch hits."""
    try:
        response = requests.get(url, params=query_params, timeout=10)
        response.raise_for_status()
        result_list.extend(response.json()['hits'])
    except requests.RequestException as e:
        print(f"Error fetching results from {url}: {e}")


def get_top_10_results(query, weight):
    """Get top 10 results from index server."""
    query_params = {'q': query, 'w': weight}
    threads = []
    results = [[] for _ in range(
        len(search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]))]
    # A list of lists to store results for each thread
    results = [[] for _ in
               range(len(search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]))]

    # Start a new thread for each index server URL, u for url
    for i, u in enumerate(search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"]):
        thread = threading.Thread(target=fetch_hits,
                                  args=(u, query_params, results[i]))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Now, merge all results and sort them using heapq.merge
    all_sorted_hits = list(merge(*results,
                                 key=lambda x: x['score'], reverse=True))

    # Return the top 10 hits
    return all_sorted_hits[:10]


@search.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""
    query = request.args.get('q', '')
    weight = request.args.get('w', 0.5)
    if query:  # Only perform the search if there is a query
        top_hits = get_top_10_results(query, weight)

        if not top_hits:
            return render_template('index.html',
                                   query=query,
                                   weight=weight, no_results=True)

        # Retrieve website details from the database
        connection = search.model.get_db()
        placeholders = ', '.join('?' for unused in top_hits)
        query_string = (
            f'SELECT docid, title, summary, url '
            f'FROM documents '
            f'WHERE docid IN ({placeholders})'
        )
        cur = connection.execute(query_string,
                                 [hit['docid'] for hit in top_hits])
        websites_dict = {row['docid']: row for row in cur.fetchall()}

        # Build the websites list maintaining the order of top_hits
        websites = [websites_dict[hit['docid']] for hit in top_hits]
        for website in websites:
            if website['summary'] == '':
                website['summary'] = 'No summary available'

        # Use the results to render the template
        return render_template('index.html', query=query,
                               weight=weight, websites=websites)

    return render_template('index.html', query='',
                           weight=weight, no_results=False, websites=[])
