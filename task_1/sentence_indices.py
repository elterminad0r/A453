"""
A script to find the locations at which a word appears in a sentence, using
1-based indexing, case insensitively.
"""

import sys

from typing import *

def locations(sentence: List[str], word: str) -> List[int]:
    """
    Find the locations of a string in a list of uppercase strings, case
    insensitively.

    Example usage:
    >>> locations(["ONE", "TWO", "THREE"], "tWo")
    [2]
    >>> locations(["ONE", "TWO", "ONE"], "one")
    [1, 3]
    >>> locations(["ASK", "NOT", "WHAT", "ASK"], "ask")
    [1, 4]
    >>> locations(["EGGS", "HAM", "SPAM", "SPAM"], "spam")
    [3, 4]
    >>> locations(["EGGS", "HAM", "SPAM", "SPAM"], "BACON")
    []

    Parameters:
    sentence - List[str] - list of uppercase strings, as returned by
     clean_sentence, to find the locations in
    word - str - string to find the location of

    Return:
    List[int] - a list of integers representing the locations at which the word
     appears
    """

    ind: int
    i: str
    return [ind for ind, i in enumerate(sentence, 1)
            if i == word.upper()]
    
def clean_sentence(sentence: str) -> List[str]:
    """
    Clean a string containing a mixed case sentence into a list of uppercase
    words.

    Example usage:
    >>> clean_sentence("OnE TWO three")
    ['ONE', 'TWO', 'THREE']
    >>> clean_sentence("Tom and JErry")
    ['TOM', 'AND', 'JERRY']
    >>> clean_sentence("python is great")
    ['PYTHON', 'IS', 'GREAT']

    Parameters:
    sentence - str - a string containing mixed case words, separated by
     spaces

    Return:
    List[str] - a list of uppercase strings
    """

    return sentence.upper().split()
    
def main() -> None:
    sentence: List[str] = clean_sentence(sys.stdin.read())
    print(f"the sentence has been parsed as {sentence}")
    #python 3.5:
    #print("the sentence has been parsed as {}".format(sentence))
    words: List[str] = sys.argv[1:]
    word: str
    for word in words:
        print(f"the word '{word}' appears at the indices "
              f"{locations(sentence, word)}")
        #print("the word '{}' appears at the indices {}"
        #      .format(word, locations(sentence, word)))
        
if __name__ == "__main__":
    main()
