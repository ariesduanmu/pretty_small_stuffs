#!/usr/bin/env python
import sys

def pattern(length):
    x = length // 3
    y = length % 3
    result = ""
    for i in range(x):
        n = i // 10
        m = i % 10
        result += 'A' + chr(n + ord('a')) + str(m)
    result += "=" * y
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage ./random_strings.py [length]")
        sys.exit(0)
    length = int(sys.argv[1])
    print(pattern(length))
