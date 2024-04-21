#!/usr/bin/env python3
"""Reduce 1."""
import sys
import re
from collections import defaultdict


def load_stopwords(filepath):
    """Load stop words from stopwords.txt."""
    with open(filepath, 'r', encoding='utf-8') as file:
        stopwords = file.read().split()
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
    """Clean up query and sort based on key."""
    inverted_index = defaultdict(lambda: defaultdict(int))
    for line in sys.stdin:
        doc_id, content = line.strip().split("\t", 1)
        parsed_terms = cleaning(content)
        for term in parsed_terms:
            inverted_index[term][doc_id] += 1

    for word, doc_ids in inverted_index.items():
        sorted_doc_ids = sorted(doc_ids.items(), key=lambda item: int(item[0]))
        for doc_id, count in sorted_doc_ids:
            # partition_key = int(doc_id) % 3
            # {partition_key}\t
            print(f"{word}\t{doc_id}\t{count}")


if __name__ == "__main__":
    main()
