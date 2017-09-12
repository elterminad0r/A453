##################################################################################

"""
A script to decompress a file compressed by bytes_compression.py - with
pointers encoded using the full range of a byte.
"""

import sys

from readable_compression import get_std_streams
from readable_decompression import decompress

from typing import *
from typing.io import *

def from_base(base: int, digits: Iterable[int]) -> int:
    """
    Convert a series of digits into an integer from a given base, where the
    digits are in reverse order

    Example usage:
    >>> from_base(2, [0, 1, 0, 1])
    10
    >>> from_base(16, [15, 15])
    255
    >>> from_base(10, [1, 2, 3])
    321

    Parameters:
    base - int - the base to convert fromm
    digits - Iterable[int] - the series of number being converted

    Return:
    int - the value of the series of digits in the given base
    """

    digit: int
    power: int
    return sum(digit * base ** power for power, digit in enumerate(digits))

def decode_pointer(pointer: bytes) -> int:
    """
    Decode a pointer encoded in a bytes object into an integer value

    Example usage:
    >>> decode_pointer(b"\xfe")
    254
    >>> decode_pointer(b"\x00\x01")
    255
    >>> decode_pointer(b"\x0f")
    15

    Parameters:
    pointer - bytes - the pointer to be decoded

    Return:
    int - the decoded pointer value
    """

    return from_base(255, pointer)

def read_dictionary(in_file: BinaryIO, separator: BinaryIO = b" ", end: BinaryIO = b"\n") -> Generator[str, None, None]:
    """
    Reads and decodes into normal strings a list of unique words from binary
    file, until newline

    Example usage:
    >>> get_input_result(read_dictionary, b"ONE TWO THREE\nabc", [], wrapper=list, binary=True)
    ['ONE', 'TWO', 'THREE']
    >>> get_input_result(read_dictionary, b"ONE\n", [], wrapper=list, binary=True)
    ['ONE']
    >>> get_input_result(read_dictionary, b"FOO BAR\n", [], wrapper=list, binary=True)
    ['FOO', 'BAR']

    Parameters:
    in_file - BinaryIO - the file to read from

    Return:
    Generator[str, None, None] - generator of words read
    """

    c: bytes = in_file.read(1)
    word: List[bytes] = []
    while c != end:
        if c == separator:
            yield b"".join(word).decode("ascii")
            word = []
        else:
            word.append(c)
        c = in_file.read(1)
    if word:
        yield b"".join(word).decode("ascii")

def read_pointers(in_file: BinaryIO) -> Generator[int, None, None]:
    """
    Read and decode pointers from binary file until EOF

    Example usage:

    >>> get_input_result(read_pointers, b"\x03\xff\x02\xff\x01", [],
    ... wrapper=list, binary=True)
    [3, 2, 1]
    >>> get_input_result(read_pointers, b"\x02", [], wrapper=list, binary=True)
    [2]
    >>> get_input_result(read_pointers, b"\xfe", [], wrapper=list, binary=True)
    [254]

    Parameters:
    in_file - BinaryIO - file to read pointers from

    Return:
    Generator[int, None, None]
    """

    c: bytes = in_file.read(1)
    n: List[bytes] = []
    while c:
        if c == b"\xff":
            yield decode_pointer(b"".join(n))
            n = []
        else:
            n.append(c)
        c = in_file.read(1)
    if n:
        yield decode_pointer(b"".join(n))

def main(stdin: BinaryIO, stdout: TextIO, argv: List[str]) -> None:
    words: List[str] = list(read_dictionary(stdin))
    pointers: List[int] = read_pointers(stdin)
    decompress(stdout, pointers, words)

if __name__ == "__main__":
    stdin: BinaryIO
    stdout: TextIO

    with get_std_streams(sys.argv, in_binary=True) as (stdin, stdout):
        main(stdin, stdout, sys.argv)
