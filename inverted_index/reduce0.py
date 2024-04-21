#!/usr/bin/env python3
"""Reduce 0."""
import sys


def main():
    """Count number of files and print it."""
    total_count = 0
    for line in sys.stdin:
        key, value = line.strip().split('\t')
        if key == "DocCount":
            total_count += int(value)
    print(total_count)
    # with open("output0", "w") as file:
    #     file.write(str(total_count) + '\n')


if __name__ == "__main__":
    main()
