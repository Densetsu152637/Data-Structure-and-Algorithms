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
    
    NO_CLUSTERING = 0
    ARRAY = 1
    SORTED_ARRAY = 2
    
COLLISION_FN_LIST = {
    CollisionResolution.NO_CLUSTERING: lambda x: [x],
    CollisionResolution.NO_CLUSTERING: lambda x: ArrayList(initial_elems=[x]),
    CollisionResolution.NO_CLUSTERING: lambda x: SortedList(initial_elems=[x])
}

PairType = Pair[K, V]
ClusterType = tuple[PairType] | ArrayList[PairType] | SortedList[PairType]

class HashMap(Generic[K, V]):
    
    @classmethod
    def pairs_from(cls, arr) -> Iterable[PairType]:
        for cluster in arr:
            cluster: ClusterType
            for pair in cluster:
                yield pair
    
    def __init__(self, 
            initial_cap: int = 21, 
            growth_rate: float = 1.618, 
            collision_resolution: CollisionResolution = CollisionResolution.ARRAY
        ):
        
        self.clusters = ArrayList[ClusterType] = ArrayList(initial_cap)
        self.growth_rate = growth_rate
        self.elems = 0
        
        self.collision_resolution = collision_resolution
        
    def __str__(self) -> str:
        return f"{self.to_dict()}"
    
    def __repr__(self) -> str:
        return self.__str__()
        
    def __len__(self) -> int:
        return self.elems 
    
    def __iter__(self):
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
        # if the number of elements is greater than the 
        # allocated space (without collisions) then we want to resize it
        if self.elems >= self.clusters.cap:
            self._resize()
            
        # search for the cluster index first        
        index = self._hash(pair.key)
        cluster: list[PairType] | None = self.clusters[index]
        
        # if our cluster exists we override it 
        if cluster == None:
            new_cluster = COLLISION_FN_LIST[self.collision_resolution](pair)
            self.clusters[index] = new_cluster
            return True
            
        # we found a cluster
        cluster_index, entry = self._get_entry_from_cluster(pair, cluster)
        
        # if our entry is null we just append it to our existing cluster
        if entry == None:
            cluster.append(entry)
            return True
        
        # if the key already exists within the cluster
        # we just override the value
        if entry.key == pair.key:
            entry.value = pair.value
            return False
        
        self.elems += 1
        
        # if we have a new key and we do not want clustering we resize until we get a vacant spot
        # so that we can insert without clustering at all
        if self.collision_resolution == CollisionResolution.NO_CLUSTERING and cluster != None:            
            while cluster != None:
                self._resize()
                index = self._hash(pair.key)
                cluster: list[PairType] | None = self.clusters[index]
                
            # at this point our cluster should be none
            new_cluster = COLLISION_FN_LIST[self.collision_resolution](pair)
            self.clusters[index] = new_cluster
            return True
        
        # we know we are safe to just append the entry to the cluster polymorphicly
        cluster.append(entry)
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

        
    
    