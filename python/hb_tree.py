"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

import numpy as np

FP_TYPE  = np.float32
INT_TYPE = np.int32

class VectorN:
    
    def __init__(self, coords: np.ndarray | list[float] | None = None, dim: int | None = None):
        
        # if both are none then give error
        if coords is None and dim is None:
            raise ValueError("KDPoint(coords, dim) both coords and dim cannot be NoneType")
        
        # guarantees that coords are a ndarray
        if isinstance(coords, list): coords = np.array(coords, dtype = FP_TYPE)
        
        dim_length = dim if dim != None else coords.size
        zero_arr: np.ndarray = np.zeros(dim_length, dtype = FP_TYPE) 
        self.coords: np.ndarray = coords if (
            coords != None 
            or (dim_length <= len(coords)) 
        ) else zero_arr
        
        # guarantees that the proper dimensions are preallocated to self.coords
        if dim != None: self.redimension(dim)
        
    def __str__(self) -> str:
        return f"VectorN(dim={self.coords.size})"
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self) -> bool:
        return self.coords.size
    
    def __eq__(self, other) -> bool:
        return isinstance(other, VectorN) and self.coords == other.coords
    
    def __getitem__(self, dim: int) -> FP_TYPE:
        if dim > self.coords.size: return None
        return self.coords[dim]
    
    def __setattr__(self, dim: int, value: FP_TYPE) -> None:
        self.coords[dim] = value
            
    def redimension(self, dim: int):
        self.coords.resize(dim)
        
    def distance_from(self, other):
        return distance_between(self, other)
        
import math
        
def distance_between(v1: VectorN, v2: VectorN) -> float:
    """
    computes the distance between two points
    in hyperdimensional space
    """
    diff = v1.coords - v2.coords
    square = diff * diff
    return math.sqrt(square.sum())
        
class HBTree:
    """
    Holey Brick Tree (hB-Tree)
    a variation on the K-D-B tree 
    a tree that is able to self balance using multiattribute indexing methods
    """
    
    def __init__(self, 
            initial_points: list[VectorN] | None = None, 
            dim: int | None = None
        ):
        pass
    
    def upsert(self, old: VectorN, new: VectorN):
        deletion = self.delete(old)
        insertion = self.insert(new)
        return (deletion, insertion)
    
    def insert(self, point: VectorN):
        pass
    
    def delete(self, point: VectorN):
        pass    
    
    def closest_to(self, point: VectorN, threshold: float):
        pass
    
    
    
    
if __name__ == "__main__":
    pass