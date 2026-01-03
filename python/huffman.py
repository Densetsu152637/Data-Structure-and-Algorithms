"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

from base import require_package

require_package("bitarray")
from bitarray import bitarray
from heap import MinHeap
import heapq

def huffman_encode(freq: dict[str, int]) -> dict[str, bitarray]:
    """
    Perform Huffman encoding on a set of character frequencies.
    Returns a dictionary {char: bitarray}.
    """
    # Step 1: Initialize the heap with leaf nodes
    heap = MinHeap(
        [(f, c, None, None) for c, f in freq.items()]
    )

    # Step 2: Iterativey merge two lowest-frequency nodes
    while len(heap) > 1:
        f1, c1, l1, r1 = heap.pop()
        f2, c2, l2, r2 = heap.pop()
        merged = (f1 + f2, c1 + c2, (c1, l1, r1), (c2, l2, r2))
        heap.append(merged)

    # Step 3: Traverse the final tree to generate bitarrays
    _, _, left, right = heap.peek()
    codes: dict[str, bitarray] = {}

    def traverse(node, prefix: bitarray):
        if node is None:
            return
        c, l, r = node
        if l is None and r is None:  # Leaf node
            codes[c] = prefix.copy()
        else:
            # should be O(1) to append a new bit 
            traverse(l, prefix + bitarray('0')) 
            traverse(r, prefix + bitarray('1'))

    traverse(left, bitarray('0'))
    traverse(right, bitarray('1'))

    return codes

def huffman_encode_string(bwt: str):
    # generate character frequency
    freq = { char: 0 for char in bwt }
    for char in bwt: freq[char] += 1     
    # return encoding of frequency
    return huffman_encode(freq)