# WEEK 2

from z_algorithm import z_algorithm

def reverse(s): 
    # O(n)
    return s[::-1]

def extended_bad_character_table(pattern: str, alphabet: set[str] = None) -> dict[str: list[int]]:
    """Preprocess pattern for the extended bad character rule."""
    if (alphabet is None):
        alphabet = set(pattern) 
        
    m = len(pattern)
    table = { char: [0] * (m + 1) for char in alphabet } 
    
    # create extended bad character table O(m * |N|)
    for i in range(m):
        char = pattern[i]
        for c in alphabet:
            table[c][i + 1] = table[c][i]
            if char == c:
                table[c][i + 1] = i + 1
                
    return table

def good_suffix_table(pattern: str) -> list[int]:
    """Preprocess pattern to create the good suffix table."""
    Z_suffix = reverse(z_algorithm(reverse(pattern)))       
    m = len(pattern)
    good_suffix = [0] * (m + 1)  
      
    for p in range(m):
        j = m - Z_suffix[p]
        good_suffix[j] = p + 1  
          
    good_suffix[0] = 0
    return good_suffix

def matched_prefix_table(pattern: str) -> list[int]:
    """Return array L where L[i] is the length of the longest prefix
    of pattern that is also a prefix of pattern[i:]."""
    m = len(pattern)
    Z = z_algorithm(pattern)
    L = [0] * (m + 1)    
    
    for i in range(m - 1, -1, -1):
        L[i] = L[i + 1]
        if i + Z[i] == m:
            L[i] = Z[i]            
    return L

def boyer_moore(text: str, pattern: str) -> list[int]:
    # pre optimisation for edge cases
    m, n = len(pattern), len(text)
    if m == 0 or n == 0 or m > n:
        return []

    bad_char       = extended_bad_character_table(pattern, set(pattern + text))
    good_suffix    = good_suffix_table(pattern)     
    matched_prefix = matched_prefix_table(pattern) 

    matches = []       # List of matches
    p = 0              # Shift of the pattern relative to back of text
    start, stop = 1, 1 # Galil optimisation window
    
    while p <= n - m:
        j = m
        
        # right-to-left scan with Galil optimisation
        while j > 1 and pattern[j - 1] == text[j - 1 + p]:
            j -= 1      
            # Galil - if you can skip within the bounds then do it
            if start <= j and j < stop:
                j = start 
                
        shift = 1
        k = j - 1
        
        full_match = False
       
        if j <= 1 and pattern[k] == text[k + p] and pattern[k + 1] == text[k + 1 + p]: 
            full_match = True
            # full match found
            matches.append(p)   
            shift = max(1, m - matched_prefix[1]) # get largest possible shift to satisfy the following iterations

        else:
            # mismatch at pattern[k] vs text[k + p]
            mismatched_char = text[k + p]

            # extended bad character rule
            brr = bad_char[mismatched_char][k]  
            bad_shift = j - brr 

            # good suffix rule                  
            good_shift = 1 
            if good_suffix[k + 1] > 0:
                good_shift = m - good_suffix[k + 1] # case 1a
            elif good_suffix[k + 1] == 0:
                good_shift = m - matched_prefix[k + 1] # case 1b       
            
            # new shift             
            shift = max(1, bad_shift, good_shift)   
            
        # Galil's optimisation with full match with k + 1 = j      
        if good_suffix[k + 1] > 0 and full_match:
            start = good_suffix[k + 1] - m + k + 1
            stop  = good_suffix[k + 1] 
            
        elif good_suffix[k + 1] <= 0 and not full_match: 
            # use matched_prefix[k + 1] (largest prefix matching suffix)
            start = 1
            stop  = matched_prefix[k + 1] 
        
        # shift characters based on found case
        p += shift

    return matches