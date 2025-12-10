"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

from sorting import radix_sort_strings, radix_sort

def lang_occ_rank(bwt: str) -> tuple[set[str], list[int], dict[str:int]]:
    # complexity: O(n)
    unique_letters = set(bwt)
    count = dict()
    rank = dict()
    occ_arr = [0] * len(bwt)
        
    for letter in unique_letters:
        count[letter] = 0
        rank[letter] = 0
    
    for (i, letter) in enumerate(bwt):
        occ_arr[i] = count[letter]
        count[letter] += 1
        
    sorted_letters = radix_sort_strings(list(unique_letters))
    
    rank[sorted_letters[0]] = 1
    
    for i in range(1, len(sorted_letters)):
        previous = rank[sorted_letters[i - 1]]
        prev_count = count[sorted_letters[i - 1]]
        rank[sorted_letters[i]] = previous + prev_count
        
    return (unique_letters, occ_arr, rank)  

def occ_dict_F(bwt: str, unique_letters: set[str]) -> dict[str:list[int]]:
    occ_dict = dict()
    
    for letter in unique_letters:
        occ_dict[letter] = [0] * (len(bwt) + 1)  
    
    for i in range(len(bwt)):
        char = bwt[i]            
        for letter in unique_letters:
            occ_dict[letter][i + 1] = occ_dict[letter][i]
            if (letter == char):
                occ_dict[letter][i + 1] += 1
                
    return occ_dict

def BWT_NAIVE(word: str) -> tuple[str, list[int]]:
    # assumes word already ends with the unique termination character
    n = len(word)
    # Generate all rotations with their original starting index
    rotations = [(word[i:] + word[:i], i) for i in range(n)]
    # Sort lexicographically by the rotated string
    sorted_rotations = radix_sort(rotations, lambda x: x[0], lambda x, pos: ord(x[pos]))
    # Extract BWT by taking the last char of each rotation
    bwt = "".join(rot[0][-1] for rot in sorted_rotations)
    # Extract suffix array: the starting indices of each sorted rotation
    SA = [rot[1] for rot in sorted_rotations]
    return bwt, SA

def BWT_INV(word: str) -> str:
    # argument should include the terminate character
    _lang, occ_arr, rank = lang_occ_rank(word)
    word_arr = [""] * len(word)
    i = 1
    for j in range(len(word) - 1, -1, -1):
        letter = word[i - 1]
        word_arr[j] = letter
        i = rank[letter] + occ_arr[i - 1]
    return "".join(word_arr[1:])

from suffix_tree import SuffixTree

def BWT_search(word: str, pattern: str) -> list[int]:
    word_p = word + "$" 
    tree = SuffixTree(word_p)
    bwt_word, SA = tree.bwt_sa()
    lang, _occ_arr, rank = lang_occ_rank(bwt_word)
    occ_dict = occ_dict_F(bwt_word, lang)
    sp, ep = 1, len(word_p) 
    
    for i in range(len(pattern) - 1, -1, -1):
        letter = pattern[i]   
        
        # reduce the bounding box size
        sp = rank[letter] + occ_dict[letter][sp - 1]
        ep = rank[letter] + occ_dict[letter][ep] - 1
                
        # early temination if bounding box becomes negative
        if sp > ep:
            break
    
    # backtracking using the suffix array to get the positions of the occurances
    return sorted(SA[sp - 1 : ep])