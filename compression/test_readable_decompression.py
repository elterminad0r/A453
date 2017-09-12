import unittest

from test_readable_compression import get_input_result, get_output_result

from readable_decompression import *

class TestReadableDecompression(unittest.TestCase):
    def test_read_dictionary(self) -> None:
        self.assertEqual(get_input_result(read_dictionary, "ONE TWO THREE\nabc",
                         [], wrapper=list), ["ONE", "TWO", "THREE"])
        self.assertEqual(get_input_result(read_dictionary, "ONE\n", [],
                         wrapper=list), ["ONE"])
        self.assertEqual(get_input_result(read_dictionary, "FOO BAR\n",
                         [], wrapper=list), ["FOO", "BAR"])
                         
    def test_read_pointers(self) -> None:
        self.assertEqual(get_input_result(read_pointers, "3 2 1", [],
                         wrapper=list), [3, 2, 1])
        self.assertEqual(get_input_result(read_pointers, "2", [],
                         wrapper=list), [2])
        self.assertEqual(get_input_result(read_pointers, "4 3", [],
                         wrapper=list), [4, 3])

    def test_decompress(self) -> None:
        self.assertEqual(get_output_result(decompress, [[1, 0], ["FOO", "BAR"]]),
                         "BAR FOO")
        self.assertEqual(get_output_result(decompress, [[0], ["FOO"]]), "FOO")
        self.assertEqual(get_output_result(decompress, [[], []]), "")


