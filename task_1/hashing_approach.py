"""
A script to find the locations at which a word appears in a sentence, but using
precomputation and hashing.
"""

import sys

from sentence_indices import locations, clean_sentence

from typing import *

def build_dictionary(sentence: List[str]) -> Dict[str, List[int]]:
    """
    Builds a dictionary of precomputed locations for the words in the sentence.

    Example usage:
    >>> build_dictionary(["ONE", "TWO", "THREE"])
    {'THREE': [3], 'TWO': [2], 'ONE': [1]}
    >>> build_dictionary(["ONE", "TWO", "ONE"])
    {'TWO': [2], 'ONE': [1, 3]}
    >>> build_dictionary(["CAT", "DOG", "DOG", "CAT"])
    {'CAT': [1, 4], 'DOG': [2, 3]}

    Parameters:
    sentence - list of strings

    Returns:
    dictionary mapping from strings to lists of integers
    """

    word: str
    return {word: locations(sentence, word) for word in sentence}

def main() -> None:
    sentence: List[str] = clean_sentence(sys.stdin.read())
    print(f"the sentence has been parsed as {sentence}")
    #print("the sentence has been parsed as {}".format(sentence))
    words: List[str] = sys.argv[1:]
    location_dict: Dict[str, List[int]] = build_dictionary(sentence)
    word: str
    for word in words:
        print(f"the word {word} appears at the indices "
              f"{location_dict[word.upper()]}")
        #print("the word {} appears at the indices {}"
        #      .format(word, location_dict[word.upper()]))
    
if __name__ == "__main__":
    main()

