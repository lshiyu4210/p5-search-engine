import flask
import os
app = flask.Flask(__name__)
# app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_00001.txt")

import index.api  # noqa: E402  pylint: disable=wrong-import-position
# Load inverted index, stopwords, and pagerank into memory
index.api.load_index()

# # ...
# import index.api
# # from index_server.index.api.api import load_index  
# from flask import Flask, jsonify
# # noqa: E402  pylint: disable=wrong-import-position

# index.api.load_index()
# # app = Flask(__name__)
# # app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")

# # def load_index():
# #     with open(inverted_index)
