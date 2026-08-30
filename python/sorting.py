"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

from typing import TypeVar, Generic

T = TypeVar("T")

# O(n^2)

def swap(arr: list[T], i: int, j: int):
    arr[i], arr[j] = arr[j], arr[i]

def bubble_sort(array: list[T]) -> list[T]:
    n = len(array)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                swap(array, j, j + 1)
                swapped = True
        # can terminate early as all elements will be in the correct ordering
        if not swapped:
            break
    return array

def selection_sort(array: list[T]) -> list[T]:
    n = len(array)
    # iterate over every element in the array
    for i in range(n):
        min_i = i
        # find minimum remaining element in unsorted position
        for j in range(i, n):
            if array[j] < array[min_i]:
                min_i = j
        # swap the next min element with i
        swap(array, i, min_i)
    return array   

def insertion_sort(array: list[T]) -> list[T]:
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        
        # shift elements to the right
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        
        array[j + 1] = key
    return array

def cycle_sort(array: list[T]) -> list[T]:
    n = len(array)
    
    for cycle_start in range(n - 1):
        item = array[cycle_start]
        
        # find where to place the item
        pos = cycle_start
        for i in range(cycle_start + 1, n):
            if array[i] < item:
                pos += 1
        
        # already in correct position
        if pos == cycle_start:
            continue
        
        # handle duplicates
        while item == array[pos]:
            pos += 1
        
        # place the item
        array[pos], item = item, array[pos]
        
        # rotate rest of the cycle
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if array[i] < item:
                    pos += 1
            
            while item == array[pos]:
                pos += 1
            
            array[pos], item = item, array[pos]
    
    return array

def cocktail_sort(array: list[T]) -> list[T]:
    n = len(array)
    start = 0
    end = n - 1
    
    while start < end:
        swapped = False
        
        # forward pass
        for i in range(start, end):
            if array[i] > array[i + 1]:
                swap(array, i, i + 1)
                swapped = True
        
        if not swapped:
            break
        
        end -= 1
        swapped = False
        
        # backward pass
        for i in range(end, start, -1):
            if array[i] < array[i - 1]:
                swap(array, i, i - 1)
                swapped = True
        
        if not swapped:
            break
        
        start += 1
    
    return array

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
    aux = [None] * len(array)  # pre-allocate once
    _merge_sort_rec(array, aux, 0, len(array))
    return array

def _merge_sort_rec(array: list[T], aux: list[T], start: int, end: int) -> None:
    # base case: length <= 1
    if end - start <= 1:
        return
    
    middle = (start + end) // 2
    
    _merge_sort_rec(array, aux, start, middle)
    _merge_sort_rec(array, aux, middle, end)
    
    _merge_arrays(array, aux, start, middle, end)

def _merge_arrays(array: list[T], aux: list[T], start: int, middle: int, end: int) -> None:
    left_i = start
    right_i = middle
    aux_i = start  # write directly into correct region of aux

    # merge into aux
    while left_i < middle and right_i < end:
        if array[left_i] <= array[right_i]:
            aux[aux_i] = array[left_i]
            left_i += 1
        else:
            aux[aux_i] = array[right_i]
            right_i += 1
        aux_i += 1

    # copy remaining left half
    while left_i < middle:
        aux[aux_i] = array[left_i]
        left_i += 1
        aux_i += 1

    # copy remaining right half
    while right_i < end:
        aux[aux_i] = array[right_i]
        right_i += 1
        aux_i += 1

    # copy back to original array
    for i in range(start, end):
        array[i] = aux[i]

def heap_sort(array: list[T]) -> list[T]:
    n = len(array)

    # Step 1: Build max heap (heapify)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(array, n, i)

    # Step 2: Extract elements one by one
    for end in range(n - 1, 0, -1):
        # swap root (max) with last element
        array[0], array[end] = array[end], array[0]
        # restore heap property on reduced heap
        _sift_down(array, end, 0)

    return array


def _sift_down(array: list[T], heap_size: int, root: int) -> None:
    while True:
        left = 2 * root + 1
        right = 2 * root + 2
        largest = root

        if left < heap_size and array[left] > array[largest]:
            largest = left
        if right < heap_size and array[right] > array[largest]:
            largest = right

        if largest == root:
            break

        array[root], array[largest] = array[largest], array[root]
        root = largest

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

