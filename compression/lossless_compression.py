##################################################################################

"""
A script to perform entirely lossless compresssion on an ascii text file, using
something similar to the prefix_code system from the lossy prefix_codes.py
"""

import sys
import string

from readable_compression import get_std_streams
from prefix_compression import (BinaryWriter, EOF, get_boundaries,
                                generate_prefix_codes, write_boundaries)
from sorted_compression import compile_dictionary, compile_pointers
from bytes_compression import write_dictionary

from typing import *
from typing.io import *

ALL_CHARS: Set[str] = {chr(i) for i in range(128)}
LETTERS: Set[str] = set(string.ascii_letters)
PUNC: Set[str] = ALL_CHARS - LETTERS

def get_runs(in_file: TextIO) -> Generator[str, None, None]:
    """
    Get runs of characters from an input file. These "runs" consist of either
    punctuation or letters, and necessarily alternate.

    Parameters:
    in_file - TextIO - file to read from
    
    Return:
    Generator[str, None, None] - a generator of runs
    """

    run: List[str] = []
    c: str = in_file.read(1)
    is_punc: bool = c in PUNC
    curr: Set[str] = PUNC if is_punc else LETTERS
    while c:
        if c in curr:
            run.append(c)
        else:
            yield "".join(run)
            run = [c]
            is_punc = not is_punc
            curr = PUNC if is_punc else LETTERS
        c = in_file.read(1)
    if run:
        yield "".join(run)

def separate_runs(runs: List[str]) -> Tuple[bool, List[str], List[str]]:
    """
    Separate a list of alternating runs into two lists, one of "words" and the
    other of punctuation. Also determines if the first run was punctuation or not.

    Parameters:
    runs - List[str] - the list of runs to be separated

    Return:
    Tuple[bool, List[str], List[str]] - a tuple of the two lists and the boolean
     indicating the type of the first run.
    """

    if runs:
        start_punc: bool = runs[0][0] in PUNC
        if start_punc:
            punc_ind: int = 0
            letter_ind: int = 1
        else:
            punc_ind: int = 1
            letter_ind: int = 0

        return start_punc, runs[letter_ind::2], runs[punc_ind::2]
    else:
        return True, [], []

def write_pointers(out_binary: BinaryWriter,
      word_pointers: Generator[int, None, None], word_codes: List[List[int]],
      punc_pointers: Generator[int, None, None], punc_codes: List[List[int]],
      start_punc: bool) -> None:
    """
    Write pointers to file. Writes pointers in alternating, fashion, as their
    respective runs were.

    Parameters:
    out_binary - BinaryWriter - BinaryWriter to write to
    word_pointers - Generator[int, None, None] - a generator of word pointers
     to be consumed
    word_codes - List[List[int]] - a list to encode word poiner values with
    punc_pointers - Generator[int, None, None] - a generator of puntuation
     pointers to be consumed
    punc - List[List[int]] - a list to encode puntuation poiner values with

    Return:
    None
    """

    out_binary.write([1] if start_punc else [0])
    while word_pointers or punc_pointers:
        try:
            if start_punc:
                out_binary.write(punc_codes[next(punc_pointers)])
                out_binary.write(word_codes[next(word_pointers)])
            else:
                out_binary.write(word_codes[next(word_pointers)])
                out_binary.write(punc_codes[next(punc_pointers)])
        except StopIteration: 
                break

def main(stdin: TextIO, stdout: BinaryIO, argv: List[str]) -> None:
    bw: binaryWriter = BinaryWriter(stdout)
    runs: List[str] = list(get_runs(stdin))
    start_punc: bool
    word: List[str]
    punc: List[str]
    start_punc, words, punc = separate_runs(runs)
    word_dict: Dict[str, int]
    keywords: List[str]
    words_dict, keywords = compile_dictionary(words)
    words_dict[EOF] = len(words_dict)
    punc_dict: Dict[str, int]
    keypunc: List[str]
    punc_dict, keypunc = compile_dictionary(punc)
    punc_dict[EOF] = len(punc_dict)
    word_boundaries: List[int] = get_boundaries(argv,
                                    len(keywords), "wboundaries")
    punc_boundaries: List[int] = get_boundaries(argv,
                                    len(keypunc), "pboundaries")
    word_codes: List[List[int]] = list(generate_prefix_codes(word_boundaries))
    punc_codes: List[List[int]] = list(generate_prefix_codes(punc_boundaries))
    word_pointers: List[int] = compile_pointers(words + [EOF], words_dict)
    punc_pointers: List[int] = compile_pointers(punc + [EOF], punc_dict)
    write_boundaries(stdout, word_boundaries)
    write_boundaries(stdout, punc_boundaries)
    write_dictionary(stdout, keywords)
    write_dictionary(stdout, keypunc, b"A", b"B")
    write_pointers(bw, word_pointers, word_codes,
                       punc_pointers, punc_codes, start_punc)
    bw.flush()

if __name__ == "__main__":
    stdin: TextIO
    stdout: BinaryIO
    with get_std_streams(sys.argv, out_binary=True) as (stdin, stdout):
        main(stdin, stdout, sys.argv)
