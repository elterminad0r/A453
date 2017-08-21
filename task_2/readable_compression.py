##################################################################################

"""
A script to perform a simplistic lossy compression on text, by creating an index
of unique words and using references to this index to store words. These
"pointers" are encoded in normal human readable base 10 numbers.
"""


import sys
import string
import argparse

from typing import *
from typing.io import *

SomeText = Union[str, bytes]

WHITESPACE: Set[str] = set(string.whitespace)
LETTERS: Set[str] = set(string.ascii_letters)

class std_streams:
    """
    An object to wrap around two file like objects, and provide boilerplate
    methods to release these files to a with statement, and clean up afterwards.
    """

    def __init__(self, stdin: IO, stdout: IO) -> None:
        self.stdin: IO = stdin
        self.stdout: IO = stdout
    
    def __enter__(self) -> Tuple[IO, IO]:
        return self.stdin, self.stdout
     
    def __exit__(self, error_type: type, value: Exception,
          traceback: "Traceback object") -> None:
        self.stdin.close()
        self.stdout.close()

    def __repr__(self) -> str:
        return "std_streams({}, {})".format(self.stdin, self.stdout)

def get_std_streams(argv: List[str], in_binary: bool = False,
      out_binary: bool = False) -> std_streams:
    """
    Get an input to read from and an output to write to, by parsing the given
    arguments, using --input and --output flags, defaulting to stdin and stdout.
    Allows binary mode to be requested.

    Example usage:
    >>> get_std_streams(["--output", "out.txt"], in_binary=True)
    std_streams(<_io.BufferedReader name='<stdin>'>,
                <_io.TextIOWrapper name='out.txt' mode='w' encoding='UTF-8'>)
    >>> get_std_streams(["--foo", "1", "3"])
    std_streams(<_io.TextIOWrapper name='<stdin>' mode='r' encoding='UTF-8'>,
                <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>)
    >>> get_std_streams([])
    std_streams(<_io.TextIOWrapper name='<stdin>' mode='r' encoding='UTF-8'>,
                <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>)
    >>> get_std_streams(["update"], in_binary=True, out_binary=True)
    std_streams(<_io.BufferedReader name='<stdin>'>,
                <_io.BufferedWriter name='<stdout>'>)

    Parameters:
    argv - List[str] - a list of strings, as might be found in sys.argv,
     representing the command line arguments to be used (and modified)
    in_binary (optional keyword argument) - bool - boolean representing whether
     the input should be in binary mode. Defaults to False
    out_binary (optional keyword argument) - bool - boolean representing whether
     the output should be in binary mode. Defaults to False

    Return:
    std_streams - a std_streams object - wraps files to be given to a context
     manager.  see std_streams documentation
    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser()                                               
    parser.add_argument("--input", type=argparse.FileType('rb' if in_binary else
                    'r'), default=(sys.stdin.buffer if in_binary else sys.stdin))
    parser.add_argument("--output", type=argparse.FileType('wb' if out_binary else
                    'w'), default=(sys.stdout.buffer if out_binary else sys.stdout))
    args: argparse.Namespace
    remaining: List[str]
    args, remaining = parser.parse_known_args(argv)
    argv[:] = remaining
    return std_streams(args.input, args.output)

def get_words(words_file: TextIO) -> Generator[str, None, None]:
    """
    Read whitespace separated words from a file. Ignores punctuation.

    Example usage (with the get_input_result helper function from test_readable_compression):
    >>> get_input_result(get_words, "One TwO THREE", [], wrapper=list)
    ['ONE', 'TWO', 'THREE']
    >>> get_input_result(get_words, "there's 1 th1ng", [], wrapper=list)
    ['THERES', 'THNG']
    >>> get_input_result(get_words, " tWo ", [], wrapper=list)
    ['TWO']
    >>> get_input_result(get_words, "", [], wrapper=list)
    []

    Parameters:
    words_file - TextIO - a text file to read strings fromm

    Return:
    Generator[str, None, None] - a generator of strings, representing words
     extracted from the file
    
    """

    word: List[str] = []
    c: str = words_file.read(1)
    while c:
        if c in LETTERS:
            word.append(c.upper())
        elif c in WHITESPACE:
            if word:
                yield "".join(word)
                word = []
        c = words_file.read(1)
    if word:
        yield "".join(word)

def compress_words(words: Iterable[str]) -> Tuple[List[str], List[int]]:
    """
    Compresses a series of words into a list of unique words and a list of
    indices for each word in the unique list.

    Example usage:
    >>> compress_words(["ONE", "TWO", "ONE"])
    (['ONE', 'TWO'], [0, 1, 0])
    >>> compress_words(["FOO", "BAR"])
    (['FOO', 'BAR'], [0, 1])
    >>> compress_words([])
    ([], [])

    Parameters:
    words - Iterable[str] - an iterable of strings, made of uppercase ascii letters

    Return:
    Tuple[List[str], List[int]] - a tuple of a list of the unique words and a list
     of words indices

    """

    words_dict: Dict[str, int] = {}
    words_list: List[str] = []
    words_size: int = 0
    pointers: List[int] = []
    word: str
    for word in words:
        if word in words_dict:
            pointers.append(words_dict[word])
        else:
            words_dict[word] = words_size
            words_list.append(word)
            pointers.append(words_size)
            words_size += 1
    return words_list, pointers

def write_dictionary(out_file: IO, words: List[str],
      separator: SomeText = " ", end: SomeText = "\n") -> None:
    """
    Writes unique words to a file, followed by a newline
    
	Example usage (with get_output_result):
	>>> get_output_result(write_dictionary, [["FOO", "BAR"]])
    "FOO BAR\n"
    >>> get_output_result(write_dictionary, [["A"]])
    "A\n"
    >>> get_output_result(write_dictionary, [[]])
    "\n"

    Parameters:
    out_file - TextIO - an output text file to write to
    words - List[str] - the list of unique words to write to file
    separator - SomeText - the the separator between words. defaults to space
    end - SomeText - the final, ending separator string to write. defaults to
     newline

    Return:
    None
    """

    out_file.write(separator.join(words) + end)

def write_pointers(out_file: TextIO, pointers: List[int], encoder: Callable[[int],
      SomeText] = str, separator: SomeText = " ") -> None:
    """
    Writes pointers to a file

    Example usage:
    >>> get_output_result(write_pointers, [[1, 2, 3]])
    "1 2 3"
    >>> get_output_result(write_pointers, [[2]])
    "2"
    >>> get_output_result(write_pointers, [[]])
    ""

    Parameters:
    out_file - TextIO - an output text file to write to
    words - List[int] - the list of pointers to write to file
    encoder - Callable[[int], Sometext] - function that encoded a an integer value
     of a pointer to SomeText

    Return:
    None
    """

    pointer: int
    out_file.write(separator.join(encoder(pointer) for pointer in pointers))

def main(stdin: TextIO, stdout: TextIO, argv: List[str]) -> None:
    words: List[str] = get_words(stdin)
    unique_words: List[str]
    pointers: List[int]
    unique_words, pointers = compress_words(words)
    write_dictionary(stdout, unique_words, " ", "\n")
    write_pointers(stdout, pointers)
    
if __name__ == "__main__":
    stdin: TextIO
    stdout: TextIO
    with get_std_streams(sys.argv) as (stdin, stdout):
        main(stdin, stdout, sys.argv)
