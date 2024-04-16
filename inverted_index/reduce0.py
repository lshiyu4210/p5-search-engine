#!/usr/bin/env python3
"""Reduce 0."""
import sys

def main():
    total_count = 0
    for line in sys.stdin:
        key, value = line.strip().split('\t')
        if key == "DocCount":
            total_count += int(value)
    print(total_count)

if __name__ == "__main__":
    main()