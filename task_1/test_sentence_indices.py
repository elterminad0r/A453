import unittest

from sentence_indices import *

class TestSentenceIndices(unittest.TestCase):
    def test_clean_sentence(self) -> None:
        self.assertEqual(clean_sentence("OnE TWO three"),
                         ["ONE", "TWO", "THREE"])
        self.assertEqual(clean_sentence("One"), ["ONE"])
        self.assertEqual(clean_sentence(""), [])
        self.assertEqual(clean_sentence(" foo "), ["FOO"])

    def test_locations(self) -> None:
        self.assertEqual(locations(["ONE", "TWO", "THREE"], "tWo"), [2])
        self.assertEqual(locations(["ONE", "TWO", "ONE"], "one"), [1, 3])
        self.assertEqual(locations(["EGGS", "HAM", "SPAM", "SPAM"], "BACON"),
                         [])
        self.assertEqual(locations([], "one"), [])
        self.assertEqual(locations(["ONE", "TWO", "THREE"], "FOUR"), [])
