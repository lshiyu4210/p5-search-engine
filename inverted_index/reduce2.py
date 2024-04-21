#!/usr/bin/env python3
"""Reduce 2."""
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""

    # """tk, idfk, di, tfik, di, ..., ..."""
    word_count = 0
    group = list(group)
    for line in group:
        word_count += 1

    for line in group:
        doc_id = line.split('\t')[1]
        key = int(doc_id) % 3
        print(str(key) + '\t' + line.strip() + '\t' + str(word_count))


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
