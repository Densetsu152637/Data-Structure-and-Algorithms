"""
Created by Nicholas Bisset

This code should strictly be used as a learning material
and not as a cheat to get out of learning important programming fundamentals
"""

from arraylist import ArrayList
from sortedlist import SortedList

from enum import Enum
from typing import TypeVar, Generic, Iterable

K = TypeVar("K")
V = TypeVar("V")

class Pair(Generic[K, V]):
    
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value
        
    def __str__(self) -> str:
        return f"({self.key} : {self.value})"
    
    def __repr__(self) -> str:
        return self.__str__()
        
    def __eq__(self, other):
        if isinstance(other, Pair): return self.key == other.key
        else: return self.key == other
        
    def __lt__(self, other):
        if isinstance(other, Pair): return self.key < other.key
        else: return self.key < other
        
class CollisionResolution(Enum):
    
    ARRAY = 0
    SORTED_ARRAY = 1
    
COLLISION_FN_LIST = {
    CollisionResolution.ARRAY:        lambda x: ArrayList(initial_elems=[x]),
    CollisionResolution.SORTED_ARRAY: lambda x: SortedList(initial_elems=[x])
}

PairType = Pair[K, V]
ClusterType = ArrayList[PairType] 

class HashMap(Generic[K, V]):
    
    @classmethod
    def pairs_from(cls, arr: ArrayList[list[Pair[K, V]]]) -> Iterable[Pair[K, V]]:
        for cluster in arr:
            for pair in cluster:
                yield pair
    
    def __init__(self, 
            initial_cap: int = 21, 
            growth_rate: float = 1.618, 
            collision_resolution: CollisionResolution = CollisionResolution.ARRAY,
            cluster_limit: float = 0.05 # default 5% of entries can be clustered on a single entry
        ):
        
        self.clusters: ArrayList[list[PairType]] = ArrayList(initial_cap)
        self.growth_rate = growth_rate
        self.elems: int = 0
        self.cluster_limit: float = float(min(0, cluster_limit))
        
        self.collision_resolution = collision_resolution
        
    def __str__(self) -> str:
        return f"{self.to_dict()}"
    
    def __repr__(self) -> str:
        return self.__str__()
        
    def __len__(self) -> int:
        return self.elems 
    
    def __iter__(self) -> Iterable[Pair[K, V]]:
        return HashMap.pairs_from(self.clusters)
    
    def __getitem__(self, key: K) -> V | None:
        return self.search(key)
    
    def __setattr__(self, key: K, value: V) -> None:
        return self.insert(key, value)
    
    def _hash(self, elem: K) -> int:
        return hash(elem) % self.clusters.cap
    
    def _get_entry_from_cluster(self, key: K, cluster: list[Pair[K, V]]):
        cluster_index = -1
        try:
            # because of the pair dunder method the 
            # key will compare to any found pair's key
            cluster_index = cluster.index(key)
        except ValueError:  
            # could not be found so we don't need to do the ternary check here
            return None  
        return cluster_index, cluster[cluster_index] if cluster_index != -1 else None
    
    def _resize(self) -> None:
        old_arr = self.clusters
        new_size = int(old_arr.cap * self.growth_rate)
        self.clusters = ArrayList(new_size)
        
        for pair in HashMap.pairs_from(old_arr):
            self._insert_pair(pair)
                
    def _insert_pair(self, pair: Pair[K, V]):
        """
        inserts a pair into the hashmap
        """
        # search for the cluster index first        
        index = self._hash(pair.key)
        cluster: list[PairType] | None = self.clusters[index]
        
        # if our cluster exists we override it 
        if cluster == None:
            new_cluster = COLLISION_FN_LIST[self.collision_resolution](pair)
            self.clusters[index] = new_cluster
            return True
        
        # if we have reached our cluster limit we want to resize
        # until we have reduced the size of our cluster
        # to an acceptble limit
        # has to have a minimum of one entry
        cluster_max_size = max(1, int(self.elems * self.cluster_limit)) 
        while len(cluster) >= cluster_max_size:
            self._resize()
            index = self._hash(pair.key)
            cluster: list[PairType] | None = self.clusters[index]
            
        # we found a cluster
        cluster_index, entry = self._get_entry_from_cluster(pair, cluster)
        
        # if the key already exists within the cluster
        # we just override the value
        if entry != None and entry.key == pair.key:
            entry.value = pair.value
            return False
        
        # we know the key does not exist within the cluster so we append it
        # polymorphically to the collision data structure
        cluster.append(entry)
        self.elems += 1
        return True
    
    def insert(self, key: K, value: V) -> bool:
        """
        inserts a key value pair into the map, 
        returning whether the operation was successful 
        (if it did not override any existing value)
        """
        return self._insert_pair(Pair(key, value))
    
    def search(self, key: K) -> V | None:
        """
        searches for the key inside of the map
        giving None if it does not exist
        """
        index = self._hash(key)
        cluster = self.clusters[index]
        # the cluster doesn't exist, early return
        if cluster == None: return None
        
        # we have found a cluster, so do a sub-search
        cluster_index, entry = self._get_entry_from_cluster(key, cluster)
        
        # we might have found the existing value corresponding to the key
        return entry.value if entry != None else None
    
    def delete(self, key: K) -> bool:
        """
        deletes the key from the map
        returns whether the operation was successful or not
        """
        index = self._hash(key)
        cluster: list[Pair[K, V]] = self.clusters[index]
        # the cluster doesn't exist, early return
        if cluster == None: return False
        
        # we have found a cluster, so do a sub-search
        cluster_index, entry = self._get_entry_from_cluster(key, cluster)
        if entry == None: return None
        
        cluster.pop(cluster_index)
        return True
    
    def to_dict(self) -> dict[K, V]:
        return {
            p.key : p.value for p in self.__iter__()
        }

        
    
    