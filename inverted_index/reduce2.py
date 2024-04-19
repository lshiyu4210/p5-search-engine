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
    # group_list = list(group)

    # nk = len(group_list)
    # doc_count_file = open("total_document_count.txt", "r")
    # N = int(doc_count_file.read())
    # doc_count_file.close()

    # norm_factor = 0
    # for line in group_list:   
    #     term_info = line.strip().split('\t')
    #     # i = cleaning(i) #['andrew', '9229752', '1']
    #     # print(term_info, nk)
    #     # partition_key = int(i[1]) % 3
    #     #idfk
    # #     idfk = math.log10(N / nk)
        
    # #     #normalization factor
    # #     temp = (int(i[2]) * idfk)**2
    # #     norm_factor += temp
    # # print(key, idfk, i[1], i[2], norm_factor)
    # print(group_list)
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
