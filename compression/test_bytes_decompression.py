import unittest

from test_readable_compression import get_input_result, get_output_result

from bytes_decompression import *

class TestBytesDecompression(unittest.TestCase):
    def test_from_base(self) -> None:
        self.assertEqual(from_base(2, [0, 1, 0, 1]), 10)
        self.assertEqual(from_base(16, [15, 15]), 255)
        self.assertEqual(from_base(10, [1, 2, 3]), 321)

    def test_decode_pointer(self) -> None:
        self.assertEqual(decode_pointer(b"\xfe"), 254)
        self.assertEqual(decode_pointer(b"\x00\x01"), 255)
        self.assertEqual(decode_pointer(b"\x0f"), 15)

    def test_read_dictionary(self) -> None:
        self.assertEqual(get_input_result(read_dictionary, b"ONE TWO THREE\nabc",
                         [], wrapper=list, binary=True), ['ONE', 'TWO', 'THREE'])
        self.assertEqual(get_input_result(read_dictionary, b"ONE\n", [],
                             wrapper=list, binary=True), ['ONE'])
        self.assertEqual(get_input_result(read_dictionary, b"FOO BAR\n", [],
                             wrapper=list, binary=True), ['FOO', 'BAR'])

    def test_read_pointers(self) -> None:
        self.assertEqual(get_input_result(read_pointers,
                 b"\x03\xff\x02\xff\x01", [], wrapper=list, binary=True), [3, 2, 1])
        self.assertEqual(get_input_result(read_pointers, b"\x02", [],
                 wrapper=list, binary=True), [2])
        self.assertEqual(get_input_result(read_pointers, b"\xfe", [],
                 wrapper=list, binary=True), [254])


