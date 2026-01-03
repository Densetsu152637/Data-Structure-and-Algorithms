"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

from typing import TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):
    
    def __init__(self, cap: int, resizeable: bool = False, initial_elems: list[T] | None = None):
        self.__array: list[T] = [None] * cap
        self.length: int = 0
        self.cap:    int = cap
        self.is_resizeable: bool = resizeable
        
        if initial_elems != None:
            for elem in initial_elems:
                self.append(elem)
                
    def __str__(self):
        return self.__array[:self.length]
    
    def __repr__(self):
        return self.__str__()
    
    def __iter__(self):
        for i in range(len(self)):
            yield self.__array[i]
    
    def __len__(self):
        return self.length
    
    def _resize(self, new_cap: int):
        if self.length < new_cap: raise ValueError(f"new cap of array of new size {new_cap} cannot be less than existing size of {self.length}")
        # create new array, copy elements over 
        # set start to 0 as we do a full iteration
        arr = [None] * new_cap 
        for i in range(len(self)):
            arr[i] = self.__array[i]
        self.__array = arr
        self.cap = new_cap
    
    def peek(self) -> T:
        return self.__array[self.length - 1]
    
    def pop(self) -> T:
        ret = self.peek()
        self.__array[self.length - 1] = None
        self.length -= 1
        return ret
    
    def append(self, item: T) -> None:
        # resize if need be
        if self.length >= self.cap and self.is_resizeable:
            self._resize(self.cap << 1)
            if not self.is_resizeable: raise RuntimeError(f"Cannot insert new item into Stack as stack is full")
            
        # insert  
        self.__array[self.length] = item
        self.length += 1

class Queue(Generic[T]):
    """
    A queue implemented using a circular cyclic list
    """
    
    def __init__(self, cap: int, resizeable: bool = False, initial_elems: list[T] | None = None):
        self.__array: list[T] = [None] * cap
        self.start:  int = 0
        self.length: int = 0
        self.cap:    int = cap
        self.is_resizeable: bool = resizeable
        
        if initial_elems != None:
            for elem in initial_elems:
                self.append(elem)
                
    def __str__(self):
        return self.__array[:self.length]
    
    def __repr__(self):
        return self.__str__()
    
    def __iter__(self):
        for i in range(len(self)):
            index = self.start + i % len(self)
            yield self.__array[index]
    
    def __len__(self):
        return self.length
    
    def _resize(self, new_cap: int):
        if self.length < new_cap: raise ValueError(f"new cap of array of new size {new_cap} cannot be less than existing size of {self.length}")
        # create new array, copy elements over 
        # set start to 0 as we do a full iteration
        arr = [None] * new_cap 
        for i, elem in enumerate(self):
            arr[i] = elem
        self.__array = arr
        self.start = 0
        self.cap = new_cap
    
    def peek(self) -> T:
        return self.__array[self.start]
    
    def serve(self) -> T:
        ret = self.peek()
        self.__array[self.start] = None
        self.start = (self.start + 1) % self.cap
        self.length -= 1
        return ret
    
    def append(self, item: T) -> None:
        # resize if need be
        if self.length >= self.cap:
            self._resize(self.cap << 1)
            if not self.is_resizeable: raise RuntimeError(f"Cannot insert new item into Stack as stack is full")
            
        # insert
        insert_index = (self.start + self.length) & self.cap
        self.__array[insert_index] = item
        self.length += 1

