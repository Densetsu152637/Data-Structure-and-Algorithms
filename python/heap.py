
from heapq import heapify
from sorting import swap
from typing import TypeVar, Generic

T = TypeVar("T")

class MinHeap(Generic[T]):
    
    def __init__(self, values: list[T] | None = None):
        self.__arr = []
        self.heapify(values)

    def __len__(self) -> int:
        return len(self.__arr)
            
    def insert(self, elem: T) -> None:
        """
        inserts an element into the heap
        """
        # appends the element to the bottom of the heap
        self.__arr.append(elem)
        # sifts the elemen up the heap
        index = len(self) - 1
        parent = (index - 1) // 2
        
        while index > 0 and self.__arr[parent] > self.__arr[index]:
            swap(self.__arr, index, parent)
            # Move up the tree to the
            # parent of the current element
            index = (index - 1) // 2
            parent = (index - 1) // 2
        
    
    def min(self) -> T:
        """
        looks at the minimum element in the heap
        """
        return self.__arr[0]
    
    def extract_min(self) -> T:
        """
        extracts the minimum element from the heap
        """
        elem = self.min()
        # swaps the max item with the min item
        swap(self.__arr, 0, -1)
        self.__arr.pop()
        
        # Heapify the tree starting from the element at the
        # deleted index
        self._heapify(0)
        return elem
    
    def heapify(self, new_elems: list[T] | None = None) -> None:
        """
        heapifies this data structure with additional elements, allowing for better time complexity 
        than inserting each element into the heap one at a time
        """
        if new_elems == None: return # no work to do
        
        # valid items to add to the heap TODO
        #self.__arr.extend(new_elems)
        #self._heapify(0)
        
    def _heapify(self, index: int) -> None:
        """
        heapifies the heap to reflect the min-heap property
        """
        while True:
        
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index

            if left_child < len(self) and self.__arr[left_child] < self.__arr[smallest]:
                smallest = left_child
                
            if right_child < len(self) and self.__arr[right_child] < self.__arr[smallest]:
                smallest = right_child

            if smallest != index:
                swap(self.__arr, index, smallest)
                index = smallest
                
            else:
                break
        
        
    
    