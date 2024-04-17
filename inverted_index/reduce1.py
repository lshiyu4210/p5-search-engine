#!/usr/bin/env python3
"""Reduce 1."""
import sys

def main():
    for line in sys.stdin:
        doc_id, content = line.strip().split("\t", 1)
        print(f"{doc_id}\t{content}\n")

if __name__ == "__main__":
    main()

