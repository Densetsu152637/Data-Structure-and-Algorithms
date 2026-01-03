"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

from base import typeof, round_up_to_nearest_power_of_two
from typing import TypeVar, Generic, Iterator

T = TypeVar("T")

class ArrayList(Generic[T]):
    
    def __init__(self, cap: int = 16, resizeable: bool = True, clip_to_power_of_two: bool = True, initial_elems: list[T] | None = None):
        #
        cap = max(cap, len(initial_elems))
        #
        self.__array: list[T] = [None] * cap
        self.length: int = 0
        self.cap:    int = cap
        self.is_resizeable:        bool = resizeable
        self.clip_to_power_of_two: bool = clip_to_power_of_two
        #
        if initial_elems != None:
            self.extend(initial_elems)
        
    def __str__(self) -> str:
        return f"ArrayList({self.length}/{self.cap}) {self.__array[:self.length]}"
    
    def __repr__(self):
        return self.__str__()
    
    def __iter__(self) -> Iterator[T]:
        return self.items()
    
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
        # if it should clip
        if self.clip_to_power_of_two:
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
    
    def items(self) -> Iterator[T]:
        """
        iterates through all non-NoneType objects within the array
        accounts for the possibility of NoneType objects being in-between 
        non-NoneType objects
        """
        exhausted = 0
        index = 0
        
        while exhausted < self.length:
            item = self[index]
            if item != None:
                yield item
                exhausted += 1
            index += 1
    
    def get(self, index: int) -> T:
        index = self._normalise_index(index) 
        if index > self.cap: raise IndexError(f"cannot access index {index} on an ArrayList of capacity {self.cap}")
        return self.__array[index]
    
    def sort(self):
        """
        creates a copy of this array and sorts that
        returns a sorted version of this object
        """
        arr = self.__array[:self.length]
        arr.sort()
        return ArrayList(self.cap, self.is_resizeable, arr)
    
    def contains(self, item: T) -> bool:
        return self.index(item) != -1
    
    def is_full(self) -> bool:
        return self.length == self.cap and not self.is_resizeable
    
    def reserve(self, amount: int):
        """
        reserves {amount} extra space to append elements freely without
        having to realloc memory
        """
        if self.cap - self.length < amount:
            self._resize(self.cap + amount)
            
    # methods which polymorphically mirror python's inbuilt list methods
    
    def append(self, item: T) -> int:
        """
        appends the item to the end of the array
        """
        return self.insert(item, -1)
    
    def pop(self, index: int = -1) -> T:
        """
        pops the item at the index from the array and returns it 
        """
        item = self[index]
        self._shuffle_and_delete(index)
        return item
    
    def remove(self, item: T) -> bool:
        """
        delete item and shuffle down elements 
        """
        deletion_index = self.index(item)
        if deletion_index == -1: return False
        self._shuffle_and_delete(deletion_index)   
        return True
            
    def extend(self, items: list[T]):
        """
        extends the list by appending the items to the array
        pre-reserves enough memory to only have to re-alloc once
        """
        self.reserve(len(items))
        for item in items: 
            if item != None:
                self.append(item)
        
    def index(self, item: T) -> int:
        """
        returns the index of the item
        if it does not exist returns -1
        """
        for i in range(len(self)):
            if self.__array[i] == item:
                return i
        return -1
    
    def insert(self, item: T, index: int) -> int:
        return self._shuffle_and_insert(item, index)
    
    