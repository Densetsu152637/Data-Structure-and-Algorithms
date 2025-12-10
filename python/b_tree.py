"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

from base import typeof
from typing import TypeVar, Generic

T = TypeVar("T")

from arraylist import ArrayList
from sortedlist import SortedList

class BNode(Generic[T]):
    
    def __init__(self, upper: int, parent = None, items: list[T] = None, children: list = None):
        """
        note that these bounds are for the number of elements in the tree rather than the 
        number of children the tree should have
        values we are going to store
        initialise with items if they exist
        """
        self.items:    SortedList[T]    = SortedList(upper,    initial_elems = items)
        self.children: ArrayList[BNode] = ArrayList(upper + 1, initial_elems = children)
        self.parent:   BNode | None     = parent
        
    def __eq__(self, other):
        return isinstance(other, BNode) and self.children == other.children and self.items == other.items

class BTree(Generic[T]):
    
    def __init__(self, t: int = 3):
        # bind level to 1 (as we must have at least one element)
        self.t = min(2, t)
        self.lower_bound = self.t - 1
        self.upper_bound = (self.t << 1) - 1
        #
        self.head = BNode(self.upper_bound)
        
    def __eq__(self, other):
        return isinstance(other, BTree) and self.head == other.head
    
    def __lt__(self, other):
        if not isinstance(other, BTree): raise ValueError(f"object {typeof(other)} is not comparable to BTree")
        return self.head < other.head
    
    def search(self, item: T) -> tuple[BNode | None, int]:        
        return self._search_node(self.head, item)
    
    def _search_node(self, node: BNode, item: T) -> tuple[BNode | None, int]:  
        """
        do a recursive binary search on items 
        to extract the entry with the highest likelihood
        if it is not found search children
        """   
        index = node.items.closest_index_of(item)
        hit: T = node.items[index]
        if hit == item: return (node, index)
        
        # get the child to recursively search from
        next_index = self._get_contested_child(node, item, index)
        next_node = node.children[next_index]
        # if we can't find it then return None
        if (next_node == None): return (None, -1)
        # next_node should be fine to search as we know it contains some values
        return self._search_node(next_node, item)    
    
    def _get_contested_child(self, node: BNode, item: T, index: int) -> int:
        hit: T = node.items[index]
        is_less_than = hit < item
        # search left or right depending on value found
        contested_index = index if is_less_than else index + 1
        return contested_index
    
    def insert(self, item: T) -> bool:
        return self._insert_into_items(self.head, item)
    
    def delete(self, item: T) -> bool:
        self._delete_from_node(self.head, item)
    
    def _is_leaf(self, node: BNode) -> bool:
        return len(node.children) == 0
    
    def _is_full(self, node: BNode) -> bool:
        return len(node.items) == self.upper_bound
    
    def _insert_item(self, node: BNode, item: T) -> bool:
        # check whether we should insert
        index = node.items.closest_index_of(item)
        hit: T = node.items[index]
        if hit == item: return False # already exists, so we don't need to insert it again      
        
        # we know now the item does not exist
        # this node will auto split if needed to
        if self._is_leaf(node):
            self._insert_into_items(node, item)
            return True
        
        # at this point we know this is not a leaf node and could be full / not full
        # we know that we have a child to insert into
        child_index = self._get_contested_child(node, item, index)
        child = node.children[child_index]
        return self._insert_item(child, item)
        
    def _insert_into_items(self, node: BNode, item: T) -> BNode:
        # if this node is full we want to split the node and promote the median
        if self._is_full(node):
            # gets the correct node to insert into the value into
            median, left, right = self._split_node(node, item)
            node = left if item < median else right
            
        # shuffle all items up by one position
        # note that we do not need to shuffle children as we only insert into leaf nodes
        node.items.append(item)
        return node
        
    def _split_node(self, node: BNode, item: T) -> tuple[T, BNode, BNode]:
        # splits the node on the median
        # creates two new child nodes that will attach to the parent
        median = node.items[self.t]
        # we need to promote the median node
        parent = node.parent
        if parent == None:
            # we know that node is self.head
            parent = BNode(self.upper_bound)
            self.head = parent
            
        # first, we need to check if parent is full, if so we split the node recursively
        # this should produce two child nodes, so we need to find out which node should be this node's parent
        if self._is_full(parent):   
            _parent_median, left_parent, right_parent = self._split_node(parent, median)
            parent = left_parent if item < median else right_parent
        
        # insert them into the correct position
        # we know that we need to insert the median inside the parent node
        # the parent will never be full at this point so it is safe to insert
        # and we take node of the index that it was inserted at, because we will
        # need to insert the children around this index in the children array
        # this is done with a binary search under the hood using the sorted list
        index = parent.items.append(median) 
        
        # we need to create two new nodes, while our current node becomes a dangling pointer (immutability)
        # which gets cleaned up automatically
        # we also need to transfer any children as node is not guaranteed to be a leaf node 100% of the time
        t_1 = self.t + 1
        left_node = BNode(
            self.upper_bound, parent,      
            items = node.items[:self.t],
            children = node.children[:t_1]
        ) # contains items/children before median
        right_node = BNode(
            self.upper_bound, parent, 
            items = node.items[t_1:],
            children = node.children[t_1:]
        ) # contains items/children after median
        
        # we want to override the left node (which is the existing index)
        # but create space for the new right node
        parent.children[index] = left_node
        parent.children.insert(right_node, index + 1)
        # we want to return the parent so that we insert into the correct child node
        return (median, left_node, right_node)
    
    def _delete_from_node(self, node: BNode, item: T) -> bool:
        index = node.items.closest_index_of(item)
        hit: T = node.items[index]
        # if we got a hit
        if hit == item: 
            # case 1: leaf node
            if self._is_leaf(node):
                # case 1a: trivial leaf node deletion (just remove the item) 
                if len(node.items) >= self.lower_bound:
                    # shuffle all items down by one position to found index, overriding it in the process
                    node.items.delete_index(index) 
                    
            # case 2: internal node and contains more than t - 1 items
            elif not self._is_leaf(node) and len(node.items) > self.lower_bound:
                predecessor: BNode = node.children[index]
                successor:   BNode = node.children[index + 1]
                # case 2a: replace with predecessor item
                if len(predecessor.items) >= self.lower_bound + 1:
                    predecessor_index = len(predecessor.items) - 1
                    node.items[index] = predecessor.items[predecessor_index], 
                    predecessor.items.delete_index(predecessor_index)
                    
                # case 2b: replace with successor item
                elif len(successor.items) > self.lower_bound + 1:
                    successor_index = 0
                    node.items[index] = successor.items[successor_index], 
                    successor.items.delete_index(successor_index)
                    
                # case 2c: merge predecesor and successor nodes together, deleting item after demoting it
                else:
                    self._merge_nodes(node, index, delete_median = True)
            
            # we were able to delete it as we found a hit
            return True
                
        # we couldn't find the item after the full sarch
        if self._is_leaf(node):
            return False
        
        # look among children (we know this is an internal node here)
        child_index = self._get_contested_child(node, item, index)
        child = node.children[child_index]
        
        # case 3: during tansversal we find a child node with exactly t - 1 elements
        if len(child.items) == self.lower_bound:
            left_sib  = node.children[child_index - 1] if child_index - 1 in range(len(node.children)) else None
            right_sib = node.children[child_index + 1] if child_index + 1 in range(len(node.children)) else None
            
            # case 3a: left sibling has at least t items
            if left_sib != None and len(left_sib.items) > self.lower_bound:
                # right rotation
                # get items from right_sib 
                left_sib_hit = left_sib.items[-1]
                left_sib_child = left_sib.children[-1]
                left_sib.items.delete_index(-1)
                left_sib.children.delete_index(-1)
                # reassign node hit value
                node.items[index] = left_sib_hit
                # put items inside found child
                child.items._shuffle_and_insert(hit, 0) # optimisation so it doesn't do a binary search (we know its the smallest item)
                child.children.insert(left_sib_child, 0) # this goes at the end so this should be in the right place anyways
            
            # case 3a*: right sibling has at least t items
            elif right_sib != None and len(right_sib.items) > self.lower_bound:
                # left rotation
                # get items from right_sib 
                right_sib_hit = right_sib.items[0]
                right_sib_child = right_sib.children[0]
                right_sib.items.delete_index(0)
                right_sib.children.delete_index(0)
                # reassign node hit value
                node.items[index] = right_sib_hit
                # put items inside found child
                child.items._shuffle_and_insert(hit, -1) # optimisation so it doesn't do a binary search (we know its the largest item)
                child.children.insert(right_sib_child, -1) # this goes at the end so this should be in the right place anyways
            
            # case 3b: left sibling has exactly t - 1 items
            elif left_sib != None and len(left_sib.items) == self.lower_bound:
                left_hit_index = child_index - 1
                child = self._merge_nodes(node, left_hit_index)
            
            # case 3b*: right sibling has exactly t - 1 items
            elif right_sib != None and len(right_sib.items) == self.lower_bound:
                right_hit_index = child_index
                child = self._merge_nodes(node, right_hit_index)
            
            # does not have any siblings but is minimum 
            # (do nothing as we cannot do anything and recurse)
        
        return self._delete_from_node(child, item)
    
    def _merge_nodes(self, parent: BNode, index: int, delete_median: bool = False) -> BNode:
        """
        merges two nodes into one via a median element, deleting and shuffling down the
        parent's child array 
        
        index should correspond to invariant: 
        parent.children[index] = left
        """
        median = parent.items[index]
        left = parent.children[index]
        right = parent.children[index + 1]  
        
        node = BNode(
            self.upper_bound, parent, 
            items = [
                *left.items,
                median if not delete_median else None, # initialiser ignores None elements
                *right.items
            ],
            children = [
                *left.children,
                *right.children
            ]
        )
        # delete item from the parent items list
        parent.items.delete_index(index)
        
        # delete right child and override left child node to merged node
        parent.children[index] = node
        parent.children.delete_index(index + 1)
        
        # if our parent node is empty now we know this is self.head
        if len(parent.items) == 0:
            node.parent = None
            self.head = node
        
        return node
                
        