"""
Script used in debugging. It examines the raw binary stdin stream as separate
bits
"""

import sys

from prefix_decompression import BinaryReader

b = BinaryReader(sys.stdin.buffer)

while True:
    print(b.read_bit(), end='')
