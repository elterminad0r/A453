##################################################################################

"""
A script to perform lossy compression on a text, encoding pointers to words
with a prefix encoding system.
"""

import sys
import itertools
import argparse
import math

from readable_compression import get_std_streams, get_words
from sorted_compression import compile_pointers, compile_dictionary
from bytes_compression import write_dictionary
from bytes_decompression import from_base

from typing import *
from typing.io import *

def get_boundaries(argv: List[str], size: int, name: str) -> List[int]:
    """
    A function to parse a set of boundaries to use for prefix encoding from
    given arguments. It also takes the size of the prefix encoding that is
    required, and will automatically generate boundaries if the user supplies
    insufficient boundaries or doesn't supply boundaries.

    Example usage:
    >>> get_boundaries(["--boundaries", "1", "2"], 3, "boundaries")
    [1, 2]
    >>> get_boundaries(["--boundaries", "4"], 3, "boundaries")
    [4]
    >>> get_boundaries(["--bounds", "82"], 400, "bounds")
    [82]
    >>> get_boundaries(["--bounds", "1", "2"], 400, "bounds")
    [2, 3, 5, 9]

    Parameters:
    args - List[str] - list of arguments to parse
    size - int - size of encoding required (largest value that needs
     to be encoded)
    name - str - name of the flag used in the arguments

    Return:
    List[int] - a list of boundaries, which are in numerical order

    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(f"--{name}", type=int, nargs="+")
    #parser.add_argument("--{}".format(name), type=int, nargs="+")
    args: argparse.Namespace
    remaining: List[str]
    args, remaining = parser.parse_known_args(argv)
    boundaries: List[int] = args.__getattribute__(name)
    argv[:] = remaining

    needs_override: bool = False

    if not boundaries:
        needs_override = True
    else:
        potential: int = sum(2 ** i for i in boundaries)
        if potential < size:
            needs_override = True
            sys.stderr.write("boundaries too small. entering defaults")
        else:
            boundaries.sort()

    if needs_override:
        largest_bound: int = int(math.log(size + 1, 2) + 1)
        boundaries = [largest_bound // 8 + 1,
                      largest_bound // 4 + 1,
                      largest_bound // 2 + 1,
                      largest_bound]

    return boundaries

EOF: int = -1

class BinaryWriter:
    """
    A class to write individual bits to a file, by handling a bit buffer, which
    is converted to a byte as soon as it reaches 8 bits
    """

    def __init__(self, out_file: BinaryIO) -> None:
        self.bit_buffer: List[int] = []
        self.out_file: BinaryIO = out_file

    def _write_bit(self, bit: int) -> None:
        self.bit_buffer.append(bit)
        if len(self.bit_buffer) == 8:
          self._write_buffer()

    def _write_buffer(self) -> None:
        self.out_file.write(bytes([from_base(2, self.bit_buffer)]))
        self.bit_buffer[:] = []
        
    def write(self, binary: Iterable[int]) -> None:
        for bit in binary:
            self._write_bit(bit)

    def flush(self) -> None:
        while self.bit_buffer:
            self._write_bit(0)

def padded_base(base: int, num: int, pad: int) -> Generator[int, None, None]:
    """
    Convert a number to a base, with padding

    Example usage:
    >>> list(padded_base(10, 123, 5))
    [3, 2, 1, 0, 0]
    >>> list(padded_base(2, 10, 6))
    [0, 1, 0, 1, 0, 0]
    >>> list(padded_base(2, 7, 6))
    [1, 1, 1, 0, 0, 0]


    Parameters:
    base - int - base to convert to
    num - int - number to convert
    pad - int - number of digits to produce

    Return:
    Generator[int, None, None] - generator of the digits in reverse order
    """



    if pad:
        quot, rem = divmod(num, base)
        yield rem
        yield from padded_base(base, quot, pad - 1)

#def get_prefix_code(n, boundaries):
#    bits = (len(boundaries) - 1).bit_length()
#
#    for ind, i in enumerate(boundaries):
#        if n.bit_length() <= i:
#            return itertools.chain(binary(ind, bits), binary(n, i))
#            break

def generate_prefix_codes(boundaries: List[int]
      ) -> Generator[List[int], None, None]:
    """
    Generate all possible prefix codes from the boundaries in a deterministic
    order

    Parameters:
    boundaries - list of given prefix boundaries

    Return:
    Generator[List[int], None, None] - generator of all possible prefix codes
    """

    bits = (len(boundaries) - 1).bit_length()
    for jnd, j in enumerate(boundaries):
        for i in range(2 ** j):
            yield list(itertools.chain(padded_base(2, jnd, bits), padded_base(2, i, j)))

def write_pointers(out_binary: BinaryWriter, pointers: List[int],
      prefix_codes: List[List[int]]) -> None:
    """
    encode a series of pointers using a given list of possible prefix codes, and
    write them to a BinaryWriter object.

    Parameters:
    out_binary - BinaryWriter - a BinaryWriter object to write to
    pointers - List[int] - a list of pointers to write

    Return:
    None
    """

    for pointer in pointers:
        out_binary.write(prefix_codes[pointer])

def write_boundaries(out_binary: BinaryIO, boundaries: List[int]) -> None:
    """
    Write some boundaries to a file, as a sort of metadata about the compression.
    It assumes that none of the boundaries are larger than 254, which for the
    purposes of compressing text is more than enough.

    Parameters:
    out_binary - BinaryIO - binary file to write to
    boundaries - List[int] - boundaries to write

    Return:
    None
    """

    out_binary.write(bytes(boundaries) + b"\xff")

def main(stdin: TextIO, stdout: BinaryIO, argv: List[int]):
    bw: BinaryWriter = BinaryWriter(stdout)
    words: List[str] = list(get_words(stdin))
    words_dict: Dict[str, int]
    keywords: List[str]
    words_dict, keywords = compile_dictionary(words)
    words_dict[EOF] = len(words_dict)
    prefix_boundaries: List[int] = get_boundaries(argv, len(keywords), "boundaries")
    prefix_codes: List[List[int]] = list(generate_prefix_codes(prefix_boundaries))
    pointers: Generator[int, None, None] = compile_pointers(words + [EOF], words_dict)
    write_boundaries(stdout, prefix_boundaries)
    write_dictionary(stdout, keywords)
    write_pointers(bw, pointers, prefix_codes)
    bw.flush()

if __name__ == "__main__":
    stdin: TextIO
    stdout: BinaryIO
    with get_std_streams(sys.argv, out_binary=True) as (stdin, stdout):
        main(stdin, stdout, sys.argv)
