##################################################################################

import sys

from readable_compression import get_std_streams
from prefix_compression import EOF
from bytes_decompression import read_dictionary
from prefix_decompression import (BinaryReader, generate_translator,
                                  read_boundaries, read_prefix_code)

from typing import *
from typing.io import *

def read_decompress(in_binary: BinaryReader, out_file: TextIO,
      word_boundaries: List[int], word_translator: Dict[str, int],
      words: List[str], punc_boundaries: List[int],
      punc_translator: Dict[str, int], punc: List[str]) -> None:
    """
    Read and decompress pointers from file

    Parameters:
    in_binary - BinaryReader - BinaryReader to read from
    out_file - TextIO - text file to write to
    word_boundaries - List[int] - prefix boundaries for words
    word_translator - Dict[str, int] - dictionary to translate from words to
     pointer values
    words - List[str] - list of unique words from which ultimately the word is
     decoded
    punc_boundaries - List[int] - prefix boundaries for punctuation
    punc_translator - Dict[str, int] - dictionary to translate from punctuation to
     pointer values
    punc - List[str] - list of unique punctuation from which ultimately the punc is
     decoded

    Return:
    None
    """

    start_punc: bool = in_binary.read_bits(1) == [1]
    while True:
        if start_punc:
            punc_code: List[int] = read_prefix_code(in_binary, punc_boundaries)
            punc_pointer: int = punc_translator[punc_code]
            punc_dec: str = punc[punc_pointer]
            if punc_dec == EOF:
                break
            out_file.write(punc_dec)

            word_code: List[int] = read_prefix_code(in_binary, word_boundaries)
            word_pointer: int = word_translator[word_code]
            word_dec: str = words[word_pointer]
            if word_dec == EOF:
                break
            out_file.write(word_dec)

        else:
            word_code: List[int] = read_prefix_code(in_binary, word_boundaries)
            word_pointer: int = word_translator[word_code]
            word_dec: str = words[word_pointer]
            if word_dec == EOF:
                break
            out_file.write(word_dec)

            punc_code: List[int] = read_prefix_code(in_binary, punc_boundaries)
            punc_pointer: int = punc_translator[punc_code]
            punc_dec: str = punc[punc_pointer]
            if punc_dec == EOF:
                break
            out_file.write(punc_dec)

def main(stdin: BinaryIO, stdout: TextIO, argv: List[str]) -> None:
    br: BinaryReader = BinaryReader(stdin)
    word_boundaries: List[int] = list(read_boundaries(stdin))
    word_translator: Dict[str, int] = generate_translator(word_boundaries)
    punc_boundaries: List[int] = list(read_boundaries(stdin))
    punc_translator: Dict[str, int] = generate_translator(punc_boundaries)
    words: List[str] = list(read_dictionary(stdin)) + [EOF]
    punc: List[str] = list(read_dictionary(stdin, b"A", b"B")) + [EOF]
    read_decompress(br, stdout, word_boundaries, word_translator, words,
                                punc_boundaries, punc_translator, punc)

if __name__ == '__main__':
    stdin: BinaryIO
    stdout: TextIO
    with get_std_streams(sys.argv, in_binary=True) as (stdin, stdout):
        main(stdin, stdout, sys.argv)
