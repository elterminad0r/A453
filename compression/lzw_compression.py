import string
import sys

from prefix_compression import BinaryWriter, padded_base

def get_pointers(in_file):
    w = ""
    c = True

    words = {i: ind for ind, i in enumerate(string.printable)}
    words_size = len(words)

    current_bits = words_size.bit_length()
    max_key = (1 << current_bits)

    for c in iter(lambda: in_file.read(1), ""):
        wc = w + c

        if wc in words:
            w = wc

        else:
            yield words[w], current_bits

            words[wc] = words_size
            words_size += 1

            if words_size == max_key:
                max_key <<= 1
                current_bits += 1

            w = c

    if w:
        yield words[w], current_bits

def write_pointers(out_binary, pointers):
    for pointer, size in pointers:
        out_binary.write(padded_base(2, pointer, size))

def main():
    bw = BinaryWriter(sys.stdout.buffer)

    pointers = get_pointers(sys.stdin)
    
    write_pointers(bw, pointers)

    bw.flush()

if __name__ == '__main__':
    main()

