
from typing import TypeVar, Generic

T = TypeVar("T")

# O(n^2)

def swap(arr: list[T], i: int, j: int):
    arr[i], arr[j] = arr[j], arr[i]

def bubble_sort(array: list[T]) -> list[T]:
    # iterate over every element in the array
    for i in range(len(array)):
        min_i = i
        # find minimum remaining element in unsorted position
        for j in range(i, len(array)):
            if array[j] < array[min_i]:
                min_i = j
        # swap the next min element with i
        swap(array, i, min_i)
    return array    

def insertion_sort(array: list[T]) -> list[T]:
    pass

# O(nlogn)

def quick_sort(array: list[T]) -> list[T]:
    _quick_sort_rec(array, 0, len(array))
    return array

def _pivot_choice(array: list[T], start: int, end: int) -> T:
    # just choose the middle element in the array
    middle  = (end + start) // 2
    pivot   = array[middle]
    return pivot

def _quick_sort_rec(array: list[T], start: int, end: int):
    # base case, length <= 1
    if end - start <= 1:
        return
    
    # inductive case
    # choose the pivot
    pivot = _pivot_choice(array, start, end)
    # 
    start_i = start
    end_i   = end
    while start_i < end_i:  
        i = start_i 
        elem = array[i]
        # put left
        if elem < pivot:
            swap(array, i, start_i)
            start_i += 1
        # put right
        else:
            swap(array, i, end_i)
            end_i -= 1
    
    # at this point we know that the pivot is in the correct position 
    _quick_sort_rec(array, start, start_i)
    _quick_sort_rec(array, start_i, end)

def merge_sort(array: list[T]) -> list[T]:
    _merge_sort_rec(array, 0, len(array))
    return array

def _merge_sort_rec(array: list[T], start: int, end: int) -> None:
    # base case, length <= 1
    if end - start < 1:
        return 
    
    # recursive inductive case
    middle = (end + start) // 2
    _merge_sort_rec(array, start, middle)
    _merge_sort_rec(array, middle, end)
    return _merge_arrays(array, start, middle, end)

def _merge_arrays(array: list[T], start: int, middle: int, end: int) -> list[T]:
    # two pointers technique
    aux = []
    left_i  = int(start)
    right_i = int(right_i)
    while left_i < middle and right_i < end:
        left_elem = array[left_i]
        right_elem = array[right_i]
        # insert left
        if left_elem < right_elem: aux.append(left_elem)
        # insert right
        else: aux.append(right_elem)
        
    # one of the lists is exhausted, now we append the remaining elements
    for l in range(left_i, middle):
        aux.append(array[l])
    for r in range(right_i, end):
        aux.append(array[r])
    # copy elements from the aux array into the main array
    for i in range(len(aux)):
        array[start + i] = aux[i]
    # explicit memory optimisation
    del aux

def heap_sort(array: list[T]) -> list[T]:
    pass

# O(n)

ALPHABET_SIZE = 256  # Extended ASCII (should work for most strings)

def radix_sort(items: list, extract, f, buckets: int) -> list[str]:
    # Find the maximum string length
    max_len = max(len(i) for i in items)
    
    # Perform counting sort for each character position (right to left)
    for pos in range(max_len - 1, -1, -1):
        # Counting sort based on character at 'pos'
        count = [[] for _ in range(buckets)]  # 
        for item in items:
            # If item is shorter, treat missing char as chr(0)
            comparable = extract(item)
            value = f(comparable, pos) if pos < len(comparable) else 0
            count[value].append(item)
        
        # Flatten count buckets back into list
        items = [item for bucket in count for item in bucket]
    
    return items

def radix_sort_strings(strings: list[str]) -> list[str]:
    return radix_sort(strings, lambda x: x, lambda x, pos: ord(x[pos]), ALPHABET_SIZE)

def radix_sort_items(items: list[list[str, T]]) -> list[list[str, T]]:
    return radix_sort(items, lambda x: x[0], lambda x, pos: ord(x[pos]), ALPHABET_SIZE)

