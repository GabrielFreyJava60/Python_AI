from typing import Any, Optional
from collections import defaultdict, OrderedDict


class DictCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.access_order = OrderedDict()
    
    def get(self, key: Any) -> Optional[Any]:
        if key in self.cache:
            self.access_order.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key: Any, value: Any) -> None:
        if self.capacity <= 0:
            return
        
        if key in self.cache:
            self.cache[key] = value
            self.access_order.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                self._evict()
            self.cache[key] = value
            self.access_order[key] = None
    
    def _evict(self) -> None:
        if not self.cache:
            return
        
        lru_key, _ = self.access_order.popitem(last=False)
        del self.cache[lru_key]


class LfuDictCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.frequencies = defaultdict(int)
        self.freq_lists = defaultdict(OrderedDict)
        self.min_freq = 0
    
    def get(self, key: Any) -> Optional[Any]:
        if key not in self.cache:
            return None
        
        self._update_frequency(key)
        return self.cache[key]
    
    def put(self, key: Any, value: Any) -> None:
        if self.capacity <= 0:
            return
        
        if key in self.cache:
            self.cache[key] = value
            self._update_frequency(key)
        else:
            if len(self.cache) >= self.capacity:
                self._evict()
            
            self.cache[key] = value
            self.frequencies[key] = 1
            self.freq_lists[1][key] = None
            self.min_freq = 1
    
    def _update_frequency(self, key: Any) -> None:
        old_freq = self.frequencies[key]
        self.frequencies[key] += 1
        new_freq = self.frequencies[key]
        
        del self.freq_lists[old_freq][key]
        self.freq_lists[new_freq][key] = None
        
        if old_freq == self.min_freq and not self.freq_lists[old_freq]:
            self.min_freq += 1
    
    def _evict(self) -> None:
        if not self.cache:
            return
        
        while not self.freq_lists[self.min_freq]:
            self.min_freq += 1
        
        freq_dict = self.freq_lists[self.min_freq]
        key_to_remove, _ = freq_dict.popitem(last=False)
        
        del self.cache[key_to_remove]
        del self.frequencies[key_to_remove]
    
    def size(self) -> int:
        return len(self.cache)
    
    def clear(self) -> None:
        self.cache.clear()
        self.frequencies.clear()
        self.freq_lists.clear()
        self.min_freq = 0
