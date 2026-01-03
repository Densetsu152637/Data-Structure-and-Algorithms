"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

from base import require_package

require_package("bitarray")
from bitarray import bitarray

def int_to_bitarray(n: int) -> bitarray:
    """Convert integer to binary as bitarray (no 0b prefix)."""
    return bitarray(bin(n)[2:])

def bit_length(n: int) -> int:
    """Return the number of bits needed to represent integer n (0 → 1)."""
    return len(int_to_bitarray(n))

def elias_encode(n: int) -> bitarray:
    """Encode a positive integer using the described Elias-style code."""
    if n <= 0:
        raise ValueError("Elias code only defined for positive integers.")

    # Start with binary representation of the integer
    code = bitarray(int_to_bitarray(n))
    
    while n > 1:
        n = bit_length(n) - 1
        n_bits = int_to_bitarray(n)
        n_bits[0] = 0 # set first bit to 1
        code = n_bits + code  # prepend
        
    # When length == 1, we replace it with a single 0
    # (so the outermost prefix starts with 0)
    return code

def elias_decode(code: bitarray) -> int:
    """Decode an Elias-style encoded bitarray back into an integer."""
    pos = 0
    # Start reading from the beginning
    length = 1

    while True:
        prefix = code[pos : pos + length]
        pos += length

        if len(prefix) == 0:
            raise ValueError("Invalid Elias code: ran out of bits.")

        if prefix[0] == 1:
            # This is the final segment — decode directly
            return int(prefix.to01(), 2)
        
        else:
            # It's a prefix — set first bit to 1, interpret, and compute new length
            prefix[0] = 1
            length = int(prefix.to01(), 2) + 1
            
if __name__ == "__main__":
    n = 561
    print("Original:", n)
    
    encoded = elias_encode(n)
    print("Encoded:", encoded.to01())

    decoded = elias_decode(encoded)
    print("Decoded:", decoded)
        