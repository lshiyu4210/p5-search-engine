#!/usr/bin/env python3
"""Map 2."""
import sys
import re

def main():
    for line in sys.stdin:
        if line.strip():
            print(line, end='')

if __name__ == "__main__":
    main()