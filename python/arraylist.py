"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

from base import typeof, round_up_to_nearest_power_of_two
from typing import TypeVar, Generic

T = TypeVar("T")

class ArrayList(Generic[T]):
    
    def __init__(self, cap: int = 16, resizeable: bool = False, initial_elems: list[T] | None = None):
        #
        cap = max(cap, len(initial_elems))
        #
        self.__array: list[T] = [None] * cap
        self.length: int = 0
        self.cap:    int = cap
        self.is_resizeable: bool = resizeable
        #
        if initial_elems != None:
            for elem in initial_elems:
                if elem != None:
                    self.append(elem)
        
    def __str__(self) -> str:
        return f"ArrayList({self.length}/{self.cap}) {self.__array[:self.length]}"
    
    def __repr__(self):
        return self.__str__()
    
    def __iter__(self):
        return ArrayListIterator(self, self.length)
    
    def __len__(self) -> bool:
        return self.length
    
    def __eq__(self, other) -> bool:
        return isinstance(other, ArrayList) and self.__array == other.__array
    
    def __add__(self, other):
        if isinstance(other, ArrayList): return ArrayList(
            self.cap + other.cap, 
            self.is_resizeable or other.is_resizeable,
            initial_elems=[
                *self.__array,
                *other.__array
            ]
        )
        
        elif isinstance(other, list): return ArrayList(
            self.cap + len(other),
            self.is_resizeable,
            initial_elems=[
                *self.__array,
                *other
            ]
        )
        
        raise ValueError(f"cannot add ArrayList and type {typeof(other)}")
    
    def __getitem__(self, index: int) -> T:
        return self.get(index)
    
    def __setattr__(self, index: int, item: T) -> None:
        index = self._normalise_index(index) 
        self.__array[index] = item
    
    def _resize(self, new_cap: int) -> None:
        # round cap up to the closest multiple of two
        new_cap = round_up_to_nearest_power_of_two(new_cap)
        if self.length < new_cap: raise ValueError(f"new cap of array of new size {new_cap} cannot be less than existing size of {self.length}")
        # create new array, copy elements over 
        arr = [None] * new_cap
        for i in range(len(self.__array)):
            arr[i] = self.__array[i]
        self.__array = arr
        self.cap = new_cap
        
    def _shuffle_and_insert(self, item: T, index: int) -> int:
        """
        inserts the item into the correct position
        asserts error if array is not resizeale and is full
        should normalise the index to an acceptible range if negative
        """
        index = self._normalise_index(index) 
        if self.length >= self.cap:
            if self.is_resizeable: self._resize(self.cap << 1)
            else: raise ValueError(f"ArrayList cannot insert additional item as array is full")
        elif index > self.length:
            raise IndexError(f"ArrayList cannot insert item to index ({index}) inside an array of length ({self.length})")
        
        # shuffles all items up to insert at the correct index
        for i in range(self.length, index, -1):
            self.__array[i + 1] = self.__array[i]
        self.__array[index] = item
        self.length += 1
        return index
        
    def _shuffle_and_delete(self, deletion_index: int) -> None:
        """
        shuffles the array down, overriding the element that needs to be deleted 
        should normalise the index to an acceptible range if negative
        """
        deletion_index = self._normalise_index(deletion_index)
        for i in range(deletion_index, self.length):
            self.__array[i] = self.__array[i + 1] 
        self.__array[self.length] = None
        self.length -= 1  
        
    def _normalise_index(self, index: int) -> int:
        """
        normalises the index such that if it is negative
        it will count from the back of the list 
        """
        return (self.length - index) % self.length if index < 0 else index % self.length
    
    def append(self, item: T) -> int:
        """
        appends the item to the end of the array
        """
        return self.insert(item, -1)
    
    def delete(self, item: T) -> bool:
        """
        delete item and shuffle down elements 
        """
        deletion_index = self.index_of(item)
        if deletion_index == -1: return False
        self._shuffle_and_delete(deletion_index)   
        return True
    
    def delete_index(self, index: int) -> bool:
        return self._shuffle_and_delete(index)
    
    def insert(self, item: T, index: int) -> int:
        return self._shuffle_and_insert(item, index)
        
    def get(self, index: int) -> T:
        index = self._normalise_index(index) 
        if index > self.cap: raise IndexError(f"cannot access index {index} on an ArrayList of capacity {self.cap}")
        return self.__array[index]
    
    def sort(self):
        """
        returns a sorted version of this object, does not mutate in place
        """
        arr = self.__array[:self.length]
        arr.sort()
        return ArrayList(self.cap, self.is_resizeable, arr)
    
    def index_of(self, item: T) -> int:
        """
        returns the index of the item
        if it does not exist returns -1
        """
        for i in range(len(self)):
            if self.__array[i] == item:
                return i
        return -1
    
    def contains(self, item: T) -> bool:
        return self.index_of(item) != -1
    
    def is_full(self) -> bool:
        return self.length == self.cap and not self.is_resizeable
    
    
    
class ArrayListIterator(Generic[T]):
    
    def __init__(self, array: ArrayList[T], length: int):
        self.__array = array
        self.index = 0
        self.stop = length
        
    def __next__(self) -> T:
        if self.index > self.stop: raise StopIteration
        ret = self.__array[self.index]
        self.index += 1
        return ret
    
    