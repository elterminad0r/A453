import unittest

from test_readable_compression import get_input_result, get_output_result

from bytes_compression import *

class TestBytesCompression(unittest.TestCase):
    def test_to_base(self) -> None:
        self.assertEqual(list(to_base(2, 10)), [0, 1, 0, 1])
        self.assertEqual(list(to_base(16, 256)), [0, 0, 1])
        self.assertEqual(list(to_base(1234, 10)), [10])
        self.assertEqual(list(to_base(2, 0)), [0])

    def test_encode_pointer(self) -> None:
        self.assertEqual(list(encode_pointer(90)), [90])
        self.assertEqual(list(encode_pointer(255)), [0, 1])
        self.assertEqual(list(encode_pointer(256)), [1, 1])
        self.assertEqual(list(encode_pointer(0)), [0])
        self.assertEqual(list(encode_pointer(255 ** 2)), [0, 0, 1])

    def test_write_dictionary(self) -> None:
        self.assertEqual(get_output_result(write_dictionary, [["FOO", "BAR"]],
                         binary=True), b"FOO BAR\n")
        self.assertEqual(get_output_result(write_dictionary, [["FOO"]],
                         binary=True), b"FOO\n")
        self.assertEqual(get_output_result(write_dictionary, [[]],
                         binary=True), b"\n")

#    def test_write_pointers(self) -> None:
#        self.assertEqual(get_output_result(write_pointers, [[1, 0, 2]],
#                         binary=True), b"\x01\xff\x00\xff\x02")
#        self.assertEqual(get_output_result(write_pointers, [[17]],
#                         binary=True), b"\x11")
#        self.assertEqual(get_output_result(write_pointers, [[254]],
#                         binary=True), b"\xfe")
#        self.assertEqual(get_output_result(write_pointers, [[255 ** 2 - 2]],
#                         binary=True), b"\xfd\xfe")
