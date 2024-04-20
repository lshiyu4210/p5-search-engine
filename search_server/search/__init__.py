"""Search package initializer."""
import flask
# import index.views

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

app.config.from_object('search.config')