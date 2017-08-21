import sys

from prefix_decompression import BinaryReader

b = BinaryReader(sys.stdin.buffer)

while True:
    print(b.read_bit(), end='')
