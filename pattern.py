#!/usr/bin/env python
import sys
import argparse

def parse_options():
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument('-l', '--length', type=int, help="length of the random string")
    parser.add_argument('-o', '--offset', type=str, help="calculate offset by segmentation fault address")
    args = parser.parse_args()
    if args.length is None and args.offset is None:
        parser.error("length or offset is needed")
    return args

def random_strings(length):
    k,l = divmod(length, 3)
    result = ""
    for i in range(0,k):
        x, y = divmod(i, 260)
        n, m = divmod(y, 10)
        result += chr(x + ord('A')) + chr(n + ord('a')) + str(m)
    result += "=" * l
    return result

def overflow_offset(offset):
    hexstr = ""
    for i in range(len(offset), 2, -2):
        c = offset[i-2:i]
        hexstr += chr(int(c, 16))
    # TODO: calculate the offset
    return hexstr

if __name__ == "__main__":
    args = parse_options()
    if args.length is not None:
         print(random_strings(int(args.length)))
    elif args.offset is not None:
         print(overflow_offset(args.offset))
