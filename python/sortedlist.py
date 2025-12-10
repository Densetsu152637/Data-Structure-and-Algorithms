
from base import typeof
from arraylist import ArrayList
from typing import TypeVar

T = TypeVar("T")

def binary_search_insert_index(arr: list[T], target: T, high: int = None) -> int:
    low = 0
    high = high if high != None else len(arr)
    
    while low < high:
        mid = (low + high) // 2
        # if we get a hit early return
        if arr[mid] == target: return mid
        # if our guess is too low
        elif arr[mid] < target: low = mid + 1
        # if our guess is too high
        else: high = mid
            
    return low

class SortedList(ArrayList[T]):
    
    def __init__(self, cap: int = 16, resizeable: bool = False, initial_elems: list[T] | None = None):
        super.__init__(self, cap, resizeable, initial_elems)
    
    def __eq__(self, other) -> bool:
        return isinstance(other, SortedList) and super().__eq__(self, other)
    
    def __add__(self, other):
        if isinstance(other, ArrayList): return SortedList(
            self.cap + other.cap, 
            self.is_resizeable or other.is_resizeable,
            initial_elems=[
                *self.__array,
                *other.__array
            ]
        )
        
        elif isinstance(other, list): return SortedList(
            self.cap + len(other),
            self.is_resizeable,
            initial_elems=[
                *self.__array,
                *other
            ]
        )
        
        raise ValueError(f"cannot add SortedList and type {typeof(other)}")
    
    def sort(self):
        # already sorted so no work needs to be done
        return self
    
    def insert(self, item: T, index: int) -> int:
        assert RuntimeError(f"cannot insert an item into a SortedList as it must remain sorted")
        
    def index_of(self, item: T) -> int:
        """
        returns the index of the item
        if it does not exist returns -1
        """
        correct_index = self.closest_index_of(item)
        return correct_index if self[correct_index] == item else -1
    
    def closest_index_of(self, item: T) -> int:
        """
        returns the closest index of where the item would live inside this list
        used for finding the correct insertion index
        """
        return binary_search_insert_index(self, item, len(self))
    
    def append(self, item: T) -> int:
        """
        appends the item into the correct position inside the array
        does a binary search to find the index to properly insert into
        """
        correct_index = self.closest_index_of(item)
        return self._shuffle_and_insert(item, correct_index)
    
    
        
        
    