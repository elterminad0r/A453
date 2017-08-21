import unittest

from test_readable_compression import get_input_result, get_output_result

from sorted_compression import *

class TestSortedCompression(unittest.TestCase):
    def test_compile_dictionary(self) -> None:
        self.assertEqual(compile_dictionary(
                         ["FOO", "BAR", "FOO", "BAR", "FOO", "EGGS"]),
            ({"FOO": 0, "BAR": 1, "EGGS": 2}, ["FOO", "BAR", "EGGS"]))
        self.assertEqual(compile_dictionary(["FOO"]),
            ({"FOO": 0}, ["FOO"]))
        self.assertEqual(compile_dictionary([]), ({}, []))

    def test_compile_pointers(self) -> None:
        self.assertEqual(list(compile_pointers(["FOO", "BAR"],
            {"FOO": 1, "BAR": 0})), [1, 0])
        self.assertEqual(list(compile_pointers(["ONE", "TWO", "ONE"],
            {"ONE": 0, "TWO": 1})), [0, 1, 0])
        self.assertEqual(list(compile_pointers([], {})), [])
