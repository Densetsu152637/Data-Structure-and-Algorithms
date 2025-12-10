"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

import math
from typing import TypeVar, Generic

T = TypeVar("T")

from base import typeof

class FibNode(Generic[T]):
    
    def __init__(self, key: T):
        # we can loosely store this
        self.key = key
        self.degree: int  = 0
        self.marked: bool = False
        self.parent: FibNode[T] | None = None
        self.left:   FibNode[T] | None = None
        self.right:  FibNode[T] | None = None
        self.child:  FibNode[T] | None = None        
        
        self.marked_for_deletion = False
    
    def __eq__(self, other):
        return isinstance(other, FibNode) and self.key == other.key
    
    def __lt__(self, other):
        if self.marked_for_deletion: return True
        if not isinstance(other, FibNode): assert ValueError(f"type {typeof(other)} is not comparable with type FibNode")
        return self.key < other.key
    
    def mark_for_deletion(self):
        self.marked_for_deletion = True

class FibHeap(Generic[T]):
    
    def __init__(self):
        self.head: FibNode[T] | None = None    
        self.count: int = 0
        
    def __len__(self) -> int:
        return self.count
    
    def __iter__(self):
        return self._rec_iterate(self.head)
            
    def empty(self) -> bool:
        return self.count == 0
    
    def min(self) -> T | None:
        return self.head.key if isinstance(self.head, FibNode) else None
        
    def insert(self, key: T) -> FibNode:
        node: FibNode[T] = FibNode(key)
        
        # if this heap is empty 
        if self.head is None:
            self.head = node
            
        # if not then we insert left
        else:
            self._insert_left(self.head, node)
            self._check_head(node)    
        
        self.count += 1
        return node            
    
    def merge(self, other_heap):
        if not isinstance(other_heap, FibHeap): assert ValueError(f"Cannot merge type {typeof(other_heap)} with FibHeap")
        
        # if we are empty simply make this point to the other heap
        if self.empty():
            self.head = other_heap.head
            self.count = other_heap.count
            
        # if the other heap is not empty then we merge
        elif not other_heap.empty():     
            self._insert_left(self.head, other_heap.head)   
            self._check_head(other_heap.head)    
                
            self.count += other_heap.count            
                
    def extract_min(self) -> T | None:
        if self.head == None: return None
        
        ret = self.head        
        self.head = self.head.right        
        child = ret.child
        
        # if our head has no neighbours
        if self.head == None:
            self.head = child # if this is None we don't really change anything
            child = None # sets it to none so _insert_left does not run
        
        if child != None:
            # we should have a valid head and child here 
            # we need to merge the ring group of the child into the main one
            self._insert_left(self.head, child)
            self._check_head(child)
        
        # always run a consolidation operation here
        self.count -= 1
        self._consolidate()
        return ret
    
    def decrease_key(self, node: FibNode[T], new_value: T):
        parent = node.parent
        # assign new value if not none (used for deletion)
        if new_value != None:
            node.key = new_value
        
        # case 1: new value is greater than parent.key, maintaining heap property (we do nothing)
        # case 2: new value is less than or equal to parent.key, violating heap property (cut and promote)
        if node < parent:
            self._rec_cut_and_promote(node)            
    
    def delete(self, node: FibNode[T]):
        node.mark_for_deletion()
        self.decrease_key(node, None)
        return self.extract_min()
    
    def search(self, value: T) -> FibNode[T] | None:
        for node in self:
            if node.key == value:
                return node
        return None
    
    def _check_head(self, new_node):
        if isinstance(new_node, FibNode) and new_node < self.head:
            self.head = new_node
                
    def _insert_left(self, node: FibNode[T], new_left: FibNode[T]):
        # inserts new_left's node group to the left of node
        # alternatively, if new_left does not have a node group then just inserts left
        curr_left  = node.left      if node.left      != None else node
        curr_right = new_left.right if new_left.right != None else new_left
        
        # couple node.left with new_left.right
        curr_right.left = curr_left
        curr_left.right = curr_right
        
        # couple node and new_left
        node.left      = new_left
        new_left.right = node
        
    def _decouple(self, node: FibNode[T]):
        l, r = node.left, node.right
        if l != None and r != None:
            l.right = r
            r.left = l        
        
    def _decouple_under(self, node: FibNode[T], new_child: FibNode[T]):
        # first decouple new_child from its neighbours
        self._decouple(new_child)
        
        # then insert the new_child underneath node
        new_child.parent = node
        if node.child == None:
            node.child = new_child  
            # we already know that this node has a degree = 0
            node.degree = new_child.degree + 1 
            
        else:
            # if the node already has a child just insert the new_child left 
            # of the current child
            self._insert_left(node.child, new_child)
            # there are a few edge cases for this degree operation, where the current child is not the 
            # highest degreem or when the current child has a greater degree than the new_child
            # or when the new_child has the greatest degree, its good to prepare for such cases
            node.degree = max(node.degree, node.child.degree + 1, new_child.degree + 1)
            # we make the child the one with the highest degree
            # for better search heuristics but this doesn't really matter, as long as the 
            # children are still always higher than the parent its fine
            if new_child.degree > node.child.degree:
                node.child = new_child
        
        
    def _consolidate(self):
        max_degree = math.ceil(math.log(len(self), 2))
        degree_table: list[FibNode[T] | None] = [None] * (max_degree + 1) # rounding up for names sake
        current: FibNode[T] = self.head
        
        while True:
            curr_degree = current.degree
            entry = degree_table[curr_degree]
            
            if entry != None:
                # we have a clash so we need to redo the heap a little
                # if our entry is less than current rather insert current underneath entry
                # to maintain our heap property
                if entry.key < current.key:
                    entry, current = current, entry
                self._decouple_under(current, entry)
            
            degree_table[current.degree] = current
            current = current.right
            
            # our stopping case, we have iterated through the entire ring
            if current == self.head or current == None:
                break
            
    def _rec_cut_and_promote(self, node: FibNode[T], rec: bool = False):
        parent = node.parent
        node.marked = False
        node.parent = None
        
        if parent == None:
            # we have reached the top after doing many case 2bs until we 
            # reached the top ring
            # we can just return here as we have no work to do
            return 
        
        if node == parent.child:
            # making sure that the children are properly managed
            parent.child = node.left
            
        self._decouple(node)
        self._insert_left(self.head, node)
        self._check_head(node)
        
        # case 2a: parent is unmarked 
        # this means we can stop here and just mark our parent
        if not parent.marked:
            # we do not have to ‘mark’ a previously
            # unmarked root (when it is a parent of a child
            # that is cut and promoted).
            # so we keep a variable if it is done recursively or not
            parent.marked = not rec
            
        # case 2b: parent is already marked
        # this means we must recursively cut parent as well
        elif parent.marked:
            self._rec_cut_and_promote(parent, True)
    
    def _rec_iterate(self, node: FibNode):
        starting = node
        not_looped = False
        while (node != starting or not_looped) and node != None:
            # iterate through current node and all children
            # before moving onto the right node
            yield node
            not_looped = True
            for n in self._rec_iterate(node.child):
                yield n
            node = node.right
    