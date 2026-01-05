"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

from typing import TypeVar, Generic, Iterator
from hashmap import HashMap

T = TypeVar("T")

class TrieNode(Generic[T]):
    
    def __init__(self, entry: T | None = None):
        # our entry for this node
        self.entry: T | None = entry
        # should have a unique hash for each character (no character clustering)
        self.children: HashMap[str, TrieNode[T]] = HashMap(
            cluster_limit = 0
        )
        
    def _iter(self, word: str):
        if self.entry:
            yield (word, self.entry)
            
        for p in self.children:
            letter, child = p.key, p.value
            for e in child._iter(word + letter):
                yield e
                
            
    def __iter__(self) -> Iterator[str, T]:
        return self._iter("")

class Trie(Generic[T]):
    
    def __init__(self, initial_elems: list[str] | None = None):
        self.head: TrieNode[T] = TrieNode()
        
        if initial_elems:
            self.insert(elem for elem in initial_elems)
    
    def __repr__(self):
        return self.__str__()
    
    def __iter__(self) -> Iterator[str, T]:
        return self.head._iter("")
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Trie) and self.head == other.head
    
    def __getitem__(self, word: str) -> T:
        return self.search(word)
    
    def __setattr__(self, word: str, value: T) -> None:
        return self.insert(word, value)    
    
    def _scaffold_down_rec(self, 
            word: str, 
            node: TrieNode[T], 
            level: int,
            on_found,
            on_no_child
        ):
        
        # we should return something here
        if len(word) == level:
            return on_found(node)
        
        # we should keep searching
        letter = word[level]
        child = node.children[letter]
        
        # the child does not exist
        if not child: child = on_no_child(node, letter)
        
        # needs a valid child object to recurse
        if not isinstance(child, TrieNode): return child
        
        # we have a valid child at this point
        return self._scaffold_down_rec(word, child, level + 1)        
    
    def insert(self, word: str, value: T) -> bool:
        """
        inserts a value along the word in the trie
        returns whether a value existed beforehand or not
        """
        # we found the place to insert the value into
        def on_found(node: TrieNode[T]):
            existed = node.entry != None
            node.entry = value
            return not existed
        
        # we need to create a new child and set it into the nodes children
        def on_no_child(node: TrieNode[T], letter: str):
            child = TrieNode()
            node.children[letter] = child
            return child
        
        return self._scaffold_down_rec(word, self.head, 0, on_found, on_no_child)
    
    def delete(self, word: str) -> bool:
        """
        deletes a value along the word in the trie
        returns whether a value was deleted or not
        """
        # we should insert into the node
        def on_found(node: TrieNode[T]):
            existed = node.entry != None
            node.entry = None
            return existed
        
        # the child does not exist, we get to return early
        def on_no_child(node: TrieNode[T], letter: str):
            return False
        
        return self._scaffold_down_rec(word, self.head, 0, on_found, on_no_child)
    
    def search(self, word: str) -> T | None:
        """
        searches for a value in the trie along the word
        """
        # we found an entry
        def on_found(node: TrieNode[T]):
            return node.entry
        
        # the child does not exist, we get to return early
        def on_no_child(node: TrieNode[T], letter: str):
            return None
        
        return self._scaffold_down_rec(word, self.head, 0, on_found, on_no_child)
    
    
    
    