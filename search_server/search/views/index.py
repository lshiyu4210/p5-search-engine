"""
Insta485 index (main) view.

URLs include:
/
"""
from flask import render_template, session, redirect, url_for
import search

@search.app.route('/')
def show_index():
    """Display / route."""
    pass