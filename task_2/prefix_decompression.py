##################################################################################

import sys

from readable_compression import get_std_streams
from prefix_compression import padded_base, from_base, generate_prefix_codes, EOF
from bytes_decompression import read_dictionary

from typing import *
from typing.io import *

class EndOfBinaryFile(Exception):
    """
    Exception for when BinaryReader reacher the end of a file
    """

    pass

class BinaryReader:
    """
    A class to read bits individually from a binary file by managing a bit buffer
    """

    def __init__(self, in_file: BinaryIO) -> None:
        self.bit_buffer: List[int] = []
        self.in_file: BinaryIO = in_file

    def _read_byte_into_buffer(self) -> None:
        byte: bytes = self.in_file.read(1)

        if not byte:
            raise EndOfBinaryFile

        self.bit_buffer = list(padded_base(2, byte[0], 8))

    def read_bit(self) -> None:
        if not self.bit_buffer:
           self._read_byte_into_buffer()

        return self.bit_buffer.pop(0)

    def read_bits(self, n: int) -> None:
        return [self.read_bit() for _ in range(n)]

def decompress(out_file: TextIO, pointers: Iterable[int], words: List[str]) -> None:
    """
    Decompress a series of pointer values, using a list of words, and write them
    to an output file.

    Parameters:
    out_file - TextIO - file to write to
    pointers - Iterable[int] - pointers to decompress
    words - List[str] - index of words to decompress them with

    Return:
    None
    """

    doSpace: bool = False
    i: int
    for i in pointers:
        dec: str = words[i]
        if dec == EOF:
            break

        if doSpace:
            out_file.write(' ')
        else:
            doSpace = True

        out_file.write(dec)

def read_prefix_code(in_binary: BinaryReader, boundaries: List[int]) -> Tuple[int]:
    """
    Read the next prefix code from file, by reading the prefix, and examining
    it to determine how far to read, and then returning the prefix along with
    the value.

    Parameters:
    in_binary - BinaryReader - BinaryReader to read bits from
    boundaries - List[int] - the list of what the boundaries are

    Return:
    Tuple[int] - this is so that this prefix code can be hashed, so its value
     can be retrieved from a dictionary
    """

    bits: int = (len(boundaries) - 1).bit_length()

    pref: List[int] = in_binary.read_bits(bits)
    pref_val: int = from_base(2, pref)
    
    return tuple(pref + in_binary.read_bits(boundaries[pref_val]))

def generate_translator(boundaries: List[int]) -> Dict[Tuple[int], int]:
    """
    Generate a dictionary from pointer tuples to their values.

    Parameters:
    boundaries - List[int] - the prefix boundaries to use

    Return:
    Dict[Tuple[int], int] - a dictionary mapping from tuples to integers, which
     are prefix codes to their values.
    """

    i: List[int]
    ind: int
    return {tuple(i): ind for ind, i in enumerate(generate_prefix_codes(boundaries))}

def read_pointers(in_binary: BinaryReader, boundaries: List[int],
      translator: Dict[Tuple[int], int]) -> Generator[int, None, None]:
    """
    Read pointers from a BinaryReader, indefinitely.

    Parameters:
    in_binary - BinaryReader - BinaryReader to read from
    boundaries - List[int] - list of boundaries to use
    translator - Dict[Tuple[int], int] - dictionary to translate prefix codes with

    Return:
    Generator[int, None, None] - generator of pointer values
    """

    while True:
        pointer: int = translator[read_prefix_code(in_binary, boundaries)]
        yield pointer

def read_boundaries(in_binary: BinaryIO) -> Generator[int, None, None]:
    """
    Read boundaries from binary file.

    Parameters:
    in_binary - BinaryIO - binary file to read from

    Return:
    Generator[int, None, None] - a generator of the boundaries found
    """

    c: bytes = in_binary.read(1)
    while c != b"\xff":
        yield ord(c)
        c = in_binary.read(1)

def main(stdin: BinaryIO, stdout: TextIO, argv: List[str]) -> None:
    br: BinaryReader = BinaryReader(stdin)
    prefix_boundaries: List[int] = list(read_boundaries(stdin))
    translator: Dict[Tuple[int], int] = generate_translator(prefix_boundaries)
    words: List[str] = list(read_dictionary(stdin)) + [EOF]
    pointers: List[int] = read_pointers(br, prefix_boundaries, translator)
    decompress(stdout, pointers, words)

if __name__ == '__main__':
    stdin: BinaryIO
    stdout: TextIO
    with get_std_streams(sys.argv, in_binary=True) as (stdin, stdout):
        main(stdin, stdout, sys.argv)
