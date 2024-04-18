#!/usr/bin/env python3
"""Reduce 2."""
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math

def reduce_one_group(key, group):
    """Reduce one group."""
    """tk, idfk, di, tfik, di, ..., ..."""
    group_list = list(group)
    nk = len(group_list)
    doc_count_file = open("total_document_count.txt", "r")
    N = int(doc_count_file.read())
    doc_count_file.close()
    
    #idfk
    idfk = math.log10(N/nk)
    
    print("key: ", key)
    print(key, idfk, nk)

def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()