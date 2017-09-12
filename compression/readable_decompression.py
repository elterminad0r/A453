##################################################################################

"""
A script to decompress output from readable_compression back into normal
(capitalised) text
"""

import sys

from readable_compression import get_std_streams, SomeText

from typing import *
from typing.io import *

def read_dictionary(in_file: TextIO, separator: SomeText = " ",
      end: SomeText = "\n") -> Generator[str, None, None]:
    """
    Read the list of unique words used as an encoding dictionary from the start of
    the compressed file, given a separator value and a value to end on.
 
    Example usage (with get_input_result helper):
    >>> get_input_result(read_dictionary, "ONE TWO THREE\nabc", [], wrapper=list)
    ['ONE', 'TWO', 'THREE']
    >>> get_input_result(read_dictionary, "ONE\n", [], wrapper=list)
    ['ONE']
    >>> get_input_result(read_dictionary, "FOO BAR\n", [], wrapper=list)
    ['FOO', 'BAR']

    Parameters:
    in_file = TextIO - file to read from
    separator - sometext - text that separates words to read. defaults to space
    end - SomeText - text htat marks the ends of words to read. defaults to newline

    Return:
    Generator[str, None, None] - a generator of word read from the file
    """


    c: str = in_file.read(1)
    word: List[str] = []
    while c != end:
        if c == separator:
            yield "".join(word)
            word = []
        else:
            word.append(c)
        c = in_file.read(1)
    if word:
        yield "".join(word)

def read_pointers(in_file: TextIO, decoder: Callable[[SomeText], int] = int,
      separator: SomeText = " ") -> Generator[int, None, None]:
    """
    Read and decode pointers from compressed file, given a separator value and
    a decoder function, which defaults to the base 10 int constructor where all
    the unique words have been consumed. Reads until EOF.
    
    Example usage:
    >>> get_input_result(read_pointers, "3 2 1", [], wrapper=list)
    [3, 2, 1]
    >>> get_input_result(read_pointers, "2", [], wrapper=list)
    [2]
    >>> get_input_result(read_pointers, "4 3", [], wrapper=list)
    [4, 3]

    Parameters:
    in_file - TextIO - file to be read from
    decoder - Callable[[SomeText], int] - decoder function to be called on each
     pointer. defaults to int constructor
    separator - SomeText - separator text between pointers. defaults to space

    Return:
    Generator[int, None, None]
    """

    c: str = in_file.read(1)
    n: List[str] = []
    while c:
        if c == separator:
            yield decoder("".join(n))
            n = []
        else:
            n.append(c)
        c = in_file.read(1)
    if n:
        yield decoder("".join(n))

def decompress(out_file: TextIO, pointers: Iterable[int], words: List[str]) -> None:
    """
    Using pointers and unique words, decompress the file and write this to a given
    output file

    Example usage:
    >>> get_output_result(decompress, [[1, 0], ["FOO", "BAR"]])
    'BAR FOO'
    >>> get_output_result(decompress, [[0], ["FOO"]])
    'FOO'
    >>> get_output_result(decompress, [[], []])
    ''

    Parameters:
    out_file - TextIO - text file to write to
    pointers - Iterable[int] - pointers to words to iterate over
    words - List[str] - words to index with pointers

    Return:
    None
    """

    do_space: bool = False
    i: int
    for i in pointers:
        if do_space:
            out_file.write(" ")
        else:
            do_space = True
        out_file.write(words[i])

def main(stdin: TextIO, stdout: TextIO, argv: List[str]) -> None:
    words: List[str] = list(read_dictionary(stdin, " ", "\n"))
    pointers: Generator[int, None, None] = read_pointers(stdin, int, " ")
    decompress(stdout, pointers, words)

if __name__ == "__main__":
    stdin: TextIO
    stdout: TextIO
    with get_std_streams(sys.argv) as (stdin, stdout):
        main(stdin, stdout, sys.argv)
