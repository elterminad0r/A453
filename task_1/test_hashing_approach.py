import unittest

from hashing_approach import *

class TestHashingApproach(unittest.TestCase):
    def test_build_dictionary(self) -> None:
        self.assertEqual(build_dictionary(["ONE", "TWO", "THREE"]), 
                         {'THREE': [3], 'TWO': [2], 'ONE': [1]})
        self.assertEqual(build_dictionary(["ONE", "TWO", "ONE"]),
                         {'TWO': [2], 'ONE': [1, 3]})
        self.assertEqual(build_dictionary(["ONE"]), {'ONE': [1]})
        self.assertEqual(build_dictionary([]), {})
