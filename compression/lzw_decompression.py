import string
import sys

from prefix_decompression import BinaryReader, EndOfBinaryFile, from_base

def read_pointers(in_binary):
    words = {ind: i for ind, i in enumerate(string.printable)}
    #words = {i: ind for ind, i in enumerate('\n' + string.ascii_uppercase)}
    words_size = len(words)

    current_bits = words_size.bit_length()
    max_key = (1 << current_bits)

    w = words[from_base(2, in_binary.read_bits(current_bits))]
    yield w

    try:
        while True:
            i = from_base(2, in_binary.read_bits(current_bits))

            if i in words:
                result = words[i]
            else:
                result = w + w[0]

            yield result

            words[words_size] = w + result[0]
            words_size += 1

            if words_size == max_key - 1:
                max_key <<= 1
                current_bits += 1


            w = result

    except EndOfBinaryFile:
        pass

def write_pointers(pointers, out_file):
    for i in pointers:
        out_file.write(i)

def main():
    br = BinaryReader(sys.stdin.buffer)

    pointers = read_pointers(br)
    write_pointers(pointers, sys.stdout)

if __name__ == '__main__':
    main()
