#!/usr/bin/env python3
"""Reduce 2."""

import math
import sys

# def calculate()

def main():

    N = 0
    with open('total_document_count.txt', 'r') as file:
        N = int(file.read())

    norm_dict = {}

    for line in sys.stdin:
        term_info = line.split('\t')
        term = term_info[0]
        doc_id_freq_pairs = term_info[1:]
        nk = len(doc_id_freq_pairs)
        idfk = math.log(N / nk)


if __name__ == "__main__":
    main()
