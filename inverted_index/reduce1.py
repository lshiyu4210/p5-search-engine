#!/usr/bin/env python3
"""Reduce 1."""
import sys
import re
from collections import defaultdict

def load_stopwords(filepath):
    """Load stop words from stopwords.txt."""
    with open(filepath, 'r') as file:
        stopwords = set(file.read().split())
    return stopwords

def cleaning(text):
    """Clean text before parsing."""
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    text = text.casefold()
    terms = text.split()
    stopwords = load_stopwords('stopwords.txt')
    cleaned_terms = [term for term in terms if term not in stopwords]

    return cleaned_terms


def main():
    inverted_index = defaultdict(set)
    for line in sys.stdin:
        doc_id, content = line.strip().split("\t", 1)
        print(f"{doc_id}\n")
        parsed_terms = cleaning(content)
        for term in parsed_terms:
            inverted_index[term].add(doc_id)

    for word, doc_ids in inverted_index.items():
        print(f"{word}\t{sorted(doc_ids)}\n")

if __name__ == "__main__":
    main()

