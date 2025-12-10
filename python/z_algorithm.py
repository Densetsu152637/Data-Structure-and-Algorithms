# WEEK 1

def z_algorithm(s: str) -> list[int]:
    """
    Compute the Z-array for the given string s.
    Z[i] = length of the longest substring starting at i
           which is also a prefix of s.
    """
    n = len(s)
    Z = [0] * n
    Z[0] = n  # Entire string matches itself
    
    # [l, r] is the window of the rightmost match
    l, r = 0, 0
    for i in range(1, n):
        if i <= r:
            # Use previously computed values to avoid re-checking characters
            Z[i] = min(r - i + 1, Z[i - l])
            
        # Try to extend match starting at i
        while i + Z[i] < n and s[Z[i]] == s[i + Z[i]]:
            Z[i] += 1
            
        # Update window if we extended past r
        if i + Z[i] - 1 > r:
            l, r = i, i + Z[i] - 1
            
    return Z
            
def z_search(text: str, pattern: str) -> list[int]:
    """
    Search for `pattern` in `text` using the Z-algorithm.
    Returns the match indexes of substrings found with pattern inside text
    """
    combined = pattern + "$" + text
    result = z_algorithm(combined)    
    # gets the pattern match values from the text segment
    match_values = result[len(pattern) + 1:]
    indexes = list(range(len(match_values)))
    # gets all the indexes of the matches according to whether they fully match the pattern 
    matches = list(filter(lambda i: match_values[i] == len(pattern), indexes))
    return matches