from typing import Any, Optional
from collections import defaultdict
import time


class DictCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.access_times = {}
    
    def get(self, key: Any) -> Optional[Any]:
        if key in self.cache:
            self.access_times[key] = time.time()
            return self.cache[key]
        return None
    
    def put(self, key: Any, value: Any) -> None:
        if self.capacity <= 0:
            return
        
        if key in self.cache:
            self.cache[key] = value
            self.access_times[key] = time.time()
        else:
            if len(self.cache) >= self.capacity:
                self._evict()
            self.cache[key] = value
            self.access_times[key] = time.time()
    
    def _evict(self) -> None:
        if not self.cache:
            return
        
        lru_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        del self.cache[lru_key]
        del self.access_times[lru_key]


class LfuDictCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.frequencies = defaultdict(int)
        self.freq_lists = defaultdict(list)
        self.access_times = {}
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
            self.freq_lists[1].append(key)
            self.access_times[key] = time.time()
            self.min_freq = 1
    
    def _update_frequency(self, key: Any) -> None:
        old_freq = self.frequencies[key]
        self.frequencies[key] += 1
        new_freq = self.frequencies[key]
        
        self.freq_lists[old_freq].remove(key)
        self.freq_lists[new_freq].append(key)
        self.access_times[key] = time.time()
        
        if old_freq == self.min_freq and not self.freq_lists[old_freq]:
            self.min_freq += 1
    
    def _evict(self) -> None:
        if not self.cache:
            return
        
        while not self.freq_lists[self.min_freq]:
            self.min_freq += 1
        
        freq_list = self.freq_lists[self.min_freq]
        
        if len(freq_list) == 1:
            key_to_remove = freq_list[0]
        else:
            key_to_remove = min(freq_list, key=lambda k: self.access_times[k])
        
        del self.cache[key_to_remove]
        del self.frequencies[key_to_remove]
        del self.access_times[key_to_remove]
        freq_list.remove(key_to_remove)
    
    def size(self) -> int:
        return len(self.cache)
    
    def clear(self) -> None:
        self.cache.clear()
        self.frequencies.clear()
        self.freq_lists.clear()
        self.access_times.clear()
        self.min_freq = 0
