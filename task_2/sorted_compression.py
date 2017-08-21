##################################################################################

"""
A script to perform lossy compression similar to readable_compression.py, but
this sorts the word by frequency, so the most frequent words have the lowst
pointer values and therefore can be encoded in less space.
"""

import sys
import collections

from readable_compression import (get_std_streams, get_words,
                                  write_dictionary, write_pointers)

from typing import *
from typing.io import *

def compile_dictionary(words: Iterable[str]) -> Tuple[Dict[str, int], List[str]]:
    """
    Compile a dictionary and list of unique words sorted by frequency, using
    collections.Counter

    Example usage:
    >>> compile_dictionary(["FOO", "BAR", "FOO", "BAR", "FOO", "EGGS"])
    ({'FOO': 0, 'BAR': 1, 'EGGS': 2}, ['FOO', 'BAR', 'EGGS'])
    >>> compile_dictionary(["FOO"])
    ({'FOO': 0}, ['FOO'])
    >>> compile_dictionary([])
    ({}, [])

    Parameters:
    words - Iterable[str] - the sequence of words to process. these should all
     be uppercase sequences of ascii letters

    Return:
    Tuple[Dict[str, int], List[str]] - a tuple of the dictionary to be used in
     compressing, and of the list of unique words in order to write to file.
    """

    c: collections.Counter = collections.Counter(words)
    words_list: List[str] = [i[0] for i in c.most_common()]
    i: str
    ind: int
    return {i: ind for ind, i in enumerate(words_list)}, words_list
    
def compile_pointers(words: List[str], words_dict: Dict[str, int]) -> Generator[int, None, None]:
    """
    Using a dictionary of words to pointers, and a list of words, convert these
    words to pointers. A relatively simple function.

    Example usage:
    >>> compile_pointers(["FOO", "BAR"], {"FOO": 1, "BAR": 0})
    [1, 0]
    >>> compile_pointers(["ONE", "TWO", "ONE"], {"ONE": 0, "TWO": 1})
    [0, 1, 0]
    >>> compile_pointers([], {})
    []

    Parameters:
    words - List[str] - the list of words to process. these should all be
     uppercase
    words_dict - Dict[str, int] - the dictionary of words to pointers

    Return:
    Generator[int, None, None] - a generator of pointers
    """

    word: str
    return (words_dict[word] for word in words)
    
def main(stdin: TextIO, stdout: TextIO, argv: List[str]) -> None:
    words: List[str] = list(get_words(stdin))
    words_dict: Dict[str, int]
    keywords: List[str]
    words_dict, keywords = compile_dictionary(words)
    pointers: Generator[int, None, None] = compile_pointers(words, words_dict)
    write_dictionary(stdout, keywords)
    write_pointers(stdout, pointers)
    
if __name__ == "__main__":
    stdin: TextIO
    stdout: TextIO
    with get_std_streams(sys.argv) as (stdin, stdout):
        main(stdin, stdout, sys.argv)
