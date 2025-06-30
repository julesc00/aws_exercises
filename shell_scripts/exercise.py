"""
check if strings are anagrams and return anagram groups.
 
Given input ["eat", "tea", "tan", "ate", "nat", "bat", "listen", "silent", "dad", "bad"]
Output [["eat", "tea", "ate"], ["tan", "nat"], ["listen", "silent"]]
"""
from typing import List

def is_anagram(text: List[str]) -> List[str]:
    to_compare = text[:]
    anagram = []
    total = []
    for word1 in text:
        for word2 in to_compare:
            r_w = word2[::-1]
            if word1 == r_w:
                anagram.append(word1)
    return anagram

if __name__ == "__main__":
    lst1 = ["eat", "tea", "tan", "ate", "nat", "bat", "listen", "silent", "dad", "bad"]
    print(is_anagram(lst1))