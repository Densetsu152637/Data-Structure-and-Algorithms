# WEEK 5 

def lz77_encode(s: str, S: int, B: int) -> list[tuple[int, int, str]]:
    """
    LZ77 encoder that outputs a list of triples (offset, length, next_char).
    - S: search window size
    - B: lookahead buffer size
    """
    triples = []
    i = 0
    n = len(s)

    while i < n:
        search_start = max(0, i - S)
        max_match_len = 0
        match_pos = -1

        # lookahead limit
        max_possible_len = min(B, n - i)

        # Find longest match in search window
        for L in range(max_possible_len, 0, -1):
            segment = s[i : i + L]
            found_at = s.rfind(segment, search_start, i)
            if found_at != -1:
                max_match_len = L
                match_pos = found_at
                break

        if max_match_len == 0:
            # No match found
            offset = 0
            length = 0
            next_char = s[i]
            i += 1
            
        else:
            offset = i - match_pos
            length = max_match_len
            if i + max_match_len < n:
                next_char = s[i + max_match_len]
                i += max_match_len + 1
            else:
                next_char = None
                i += max_match_len

        triples.append((offset, length, next_char))

    return triples 


def lz77_decode(triples):
    """
    Reconstruct the original string from a list of (offset, length, next_char) triples.
    """
    output = []

    for offset, length, next_char in triples:
        if offset == 0:
            # No match — just add the literal
            if next_char is not None:
                output.append(next_char)
        else:
            # Copy substring from already decoded output
            start = len(output) - offset
            for _ in range(length):
                output.append(output[start])
                start += 1
            # Then append the next literal (if any)
            if next_char is not None:
                output.append(next_char)

    return ''.join(output)


if __name__ == "__main__":
    s = "aacaacabcabaaac"
    triples = lz77_encode(s, 4, 4) 
    decompressed = lz77_decode(triples)
    print(f"s: {s}\nd: {decompressed}\nsuccess? {s == decompressed}\ntriples: {triples}")