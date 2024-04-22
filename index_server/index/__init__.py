"""Index server init."""
import os
import pathlib
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
app.config["FILE_PATH"] = pathlib.Path(__file__).resolve().parent
app.config["DICT_PATH"] = app.config["FILE_PATH"] / \
    'inverted_index' / app.config["INDEX_PATH"]


stopword_set = None
pagerank_list = None
index_list = None
doc_N_factor = None

import index.api  # noqa: E402  pylint: disable=wrong-import-position
# Load inverted index, stopwords, and pagerank into memory
index.api.load_index()
