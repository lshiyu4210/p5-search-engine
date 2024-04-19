import flask

app = flask.Flask(__name__)

@app.route("/api/v1/")
def get_index():
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)

