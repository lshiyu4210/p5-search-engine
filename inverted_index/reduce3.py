#!/usr/bin/env python3
"""Reduce 3."""

import sys
import math
from collections import defaultdict


def main():
    """Calculate output entries."""
    n_val = 0
    with open("total_document_count.txt", "r", encoding='utf-8') as file:
        n_val = int(file.read())

    norm_factor = 0.0
    norm_dict = defaultdict(float)
    doc_id = None
    output_dict = defaultdict(list)
    for line in sys.stdin:
        line = line.partition('\t')[2]
        line = line.strip()
        parts = line.split('\t')

        key = parts[0]
        temp_doc_id = parts[1]
        # reset new doc_id
        if temp_doc_id != doc_id:
            if doc_id is not None:
                norm_dict[int(doc_id)] += norm_factor
                # print(norm_dict[int(doc_id)])
            norm_factor = 0.0
            doc_id = temp_doc_id

        # tf-idf calculation
        idfk = math.log10(n_val / float(parts[3]))
        tfik = int(parts[2])
        wik = tfik * idfk
        if output_dict[key]:
            output = [int(parts[1]), tfik]
        else:
            output = [idfk, int(parts[1]), tfik]
        output_dict[key].append(output)
        norm_factor += wik * wik
    if doc_id and doc_id.isdigit():
        norm_dict[int(doc_id)] += norm_factor
    else:
        print(f"Warning: Invalid doc_id encountered: {doc_id}")

    for key, output_list in sorted(output_dict.items()):
        message = f"{key} "
        for row in output_list:
            if len(row) == 2:
                message += " ".join(str(x) for x in row)
                message += " "
                message += str(norm_dict[row[0]]) + " "
            elif len(row) == 3:
                message += " ".join(str(x) for x in row)
                message += " "
                message += str(norm_dict[row[1]]) + " "
        print(message)


if __name__ == "__main__":
    main()
