import unittest

from io import StringIO, BytesIO

from readable_compression import *

from typing import *

def get_output_result(func: Callable[..., None], args: Iterable[Any],
      binary: bool = False) -> Union[str, bytes]:
    """
    A function to simulate an output file for another function, using a StringIO
    or BytesIO object, and return the contents of the file after processing. It
    assumes the file object is the first argument to the function, and it can take
    remaining arguments to be passed.

    Example usage:
    >>> def f(out_file):
    ...     out_file.write("foo")
    >>> get_output_result(f, [])
    "foo"
    >>> def g(out_file, n):
    ...     out_file.write(str(n + 1))
    >>> get_output_result(g, [2])
    "3"

    Parameters:
    func - Callable[..., None] - function which will process the file
    args - Iterable[Any] - remaining arguments for func
    binary - bool - boolean determining whether the file should be binary, ie
     whether BytesIO or StringIO should be used

    Return:
    Union[str, bytes] - The contents of the processed file. either str or bytes
     depending on the value of binary
    """

    output: IO = BytesIO() if binary else StringIO() 
    func(output, *args)
    return output.getvalue()

def get_input_result(func: Callable[..., Any], in_val: Union[str, bytes], args:
      Iterable[Any], wrapper: Callable[[Any], Any] = lambda x: x,
      binary: bool = False) -> Any:
    """
    A function to simulate an input file for another function, using a StringIO or
    BytesIO object, and return the return value of the function, allowing for this
    to be passed through a wrapper function. It assumes the file object is the
    first argument to the function, and it can take remaining arguments to be
    passed.

    Example usage (these are somewhat contrived):
    >>> def f(in_file):
    ...     return in_file.read() + "bar"
    >>> get_input_result(f, "foo", [])
    "foobar"
    >>> def g(binary_file, increment):
    ...     return [ord(binary_file.read(1)) + increment]
    >>> get_input_result(g, b"\x80", [2], binary=True, wrapper=bytes)
    b"\x82"

    Parameters:
    func - Callable[..., Any] - the function which will take input from the file
    in_val - Union[str, bytes] - the contents of the file. Type depends on the
     value of binary
    args - Iterable[Any] - remaining arguments to pass to the file
    wrapper - Callable[[Any], [Any]] - optional wrapper function, defaults to
     an identity operator
    binary - bool - boolean signifying whether it is a binary or text file.
     defaults to False

    Return:
    Any - the return value of the wrapper function applied to the return value
     of the function
    """

    in_file: IO = (BytesIO if binary else StringIO)(in_val)
    return wrapper(func(in_file, *args))

class TestReadableCompression(unittest.TestCase):
    def test_get_words(self) -> None:
        self.assertEqual(get_input_result(get_words, "One TwO THREE", [],
                             wrapper=list), ["ONE", "TWO", "THREE"])
        self.assertEqual(get_input_result(get_words, "", [], wrapper=list), [])
        self.assertEqual(get_input_result(get_words, "  ", [], wrapper=list), [])
        self.assertEqual(get_input_result(get_words, " TwO ", [], wrapper=list),
                         ["TWO"])
        self.assertEqual(get_input_result(get_words, "there's 1 th1ng", [],
                            wrapper=list), ["THERES", "THNG"])

    def test_compress_words(self) -> None:
        self.assertEqual(compress_words(["ONE", "TWO", "ONE"]), (["ONE", "TWO"],
                         [0, 1, 0]))
        self.assertEqual(compress_words(["ONE"]), (["ONE"], [0]))
        self.assertEqual(compress_words([]), ([], []))

    def test_write_dictionary(self) -> None:
        self.assertEqual(get_output_result(write_dictionary, [["FOO", "BAR"],
                         " ", "\n"]), "FOO BAR\n")
        self.assertEqual(get_output_result(write_dictionary, [["A"],
                         " ", "\n"]), "A\n")
        self.assertEqual(get_output_result(write_dictionary, [[],
                         " ", "\n"]), "\n")
        
    def test_write_pointers(self) -> None:
        self.assertEqual(get_output_result(write_pointers, [[1, 2, 3]]), "1 2 3")
        self.assertEqual(get_output_result(write_pointers, [[2]]), "2")
        self.assertEqual(get_output_result(write_pointers, [[]]), "")
