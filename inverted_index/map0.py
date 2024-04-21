#!/usr/bin/env python3
"""Map 0."""
import sys
import re


def main():
    """Count number of HTMI files based on tag."""
    pattern = re.compile(r'<!DOCTYPE html>', re.IGNORECASE)
    for line in sys.stdin:
        if pattern.search(line):
            print('DocCount\t1')


if __name__ == "__main__":
    main()
