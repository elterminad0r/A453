##################################################################################

"""
A script to compress a file similarly to sorted_compression.py, but using the
full range of a byte to encode a pointer
"""

import sys

from readable_compression import get_std_streams, get_words, write_pointers
from sorted_compression import compile_pointers, compile_dictionary

from typing import *
from typing.io  import *

def to_base(base: int, num: int) -> Generator[int, None, None]:
    """
    Convert a number to a base, using a recursive algorithm to find the last
    digit. Returns digits in reverse order

    Example usage:
    >>> list(to_base(2, 10))
    [0, 1, 0, 1]
    >>> list(to_base(16, 256))
    [0, 0, 1]
    >>> list(to_base(1234, 10))
    [10]
    >>> list(to_base(2, 0))
    [0]

    Parameters:
    base - int - value of the base to convert to
    num - int - number to be converted

    Return:
    Generator[int, None, None] - a generator of integers, which are digits in
     reverse order
    """

    quot: int
    rem: int
    quot, rem = divmod(num, base)
    yield rem
    if quot:
        yield from to_base(base, quot)

def encode_pointer(pointer: int) -> bytes:
    """
    Encode a pointer value to bytes. Converts number to base 255 and constructs
    a bytes object.

    Example usage (converting back to list for visual clarity):
    >>> list(encode_pointer(90))
    [90]
    >>> list(encode_pointer(255))
    [0, 1]
    >>> list(encode_pointer(256))
    [1, 1]
    >>> list(encode_pointer(0))
    [0]
    >>> list(encode_pointer(255 ** 2))
    [0, 0, 1]

    Parameters:
    pointer - int - the pointer value to be converted

    Return:
    bytes - the pointer encoded in a bytes object, which can be written to a
     file
    """

    return bytes(to_base(255, pointer))
    
def write_dictionary(bin_out: BinaryIO, words: List[str], separator: BinaryIO = b" ", end: BinaryIO = b"\n") -> None:
    """
    Write string words to a binary file, followed by a newline

    Example usage:
    >>> get_output_result(write_dictionary, [["FOO", "BAR"]], binary=True)
    b'FOO BAR\n'
    >>> get_output_result(write_dictionary, [["FOO"]], binary=True)
    b'FOO\n'
    >>> get_output_result(write_dictionary, [[]], binary=True)
    b'\n'

    Parameters:
    bin_out - BinaryIO - binary file to write to
    words - List[str] - list of words to write
    separator - BinaryIO - separator value between words

    Return:
    None
    """

    i: str
    bin_out.write(separator.join(bytes(i, encoding="ascii") for i in words) + end)

def main(stdin: TextIO, stdout: BinaryIO, argv: List[str]):
    words: List[str] = list(get_words(stdin))
    words_dict: Dict[str, int]
    keywords: List[str]
    words_dict, keywords = compile_dictionary(words)
    pointers: List[int] = compile_pointers(words, words_dict)
    write_dictionary(stdout, keywords)
    write_pointers(stdout, pointers, encode_pointer, b"\xff")

if __name__ == "__main__":
    stdin: TextIO
    stdout: BinaryIO
    with get_std_streams(sys.argv, out_binary=True) as (stdin, stdout):
        main(stdin, stdout, sys.argv)
