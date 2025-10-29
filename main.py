from typing import Optional, Callable, Iterator
import random


class RandomNumbersStream:
    def __init__(self, min: int = -10 ** 20, max: int = 10 ** 20):
        if min > max:
            raise ValueError(f"min ({min}) must be <= max ({max})")
        
        self.min = min
        self.max = max
        self.filter_predicate: Optional[Callable[[int], bool]] = None
        self.limit: Optional[int] = None
        self.distinct = False
        # Cache the range size to avoid recomputation
        self._range_size: int = self.max - self.min + 1
    
    def setFilter(self, predicate: Callable[[int], bool]) -> None:
        self.filter_predicate = predicate
    
    def setLimit(self, limit: int) -> None:
        if limit < 0:
            raise ValueError(f"limit must be >= 0, got {limit}")
        self.limit = limit
    
    def setDistinct(self) -> None:
        self.distinct = True
    
    def resetDistinct(self) -> None:
        self.distinct = False
    
    def _passes_filter(self, num: int) -> bool:
        if self.filter_predicate is None:
            return True
        try:
            return self.filter_predicate(num)
        except Exception:
            return False
    
    def _generate_next(self, used_numbers: set[int]) -> Optional[int]:
        max_attempts = max(10000, self._range_size * 10)
        
        for _ in range(max_attempts):
            num = random.randint(self.min, self.max)
            
            if self.distinct and num in used_numbers:
                continue
            
            if not self._passes_filter(num):
                continue
            
            if self.distinct:
                used_numbers.add(num)
            return num
        
        return None
    
    def __iter__(self) -> Iterator[int]:
        # Fast path: distinct without filter can be generated in O(k)
        if self.distinct and self.filter_predicate is None:
            k = self._range_size if self.limit is None else min(self.limit, self._range_size)
            for num in random.sample(range(self.min, self.max + 1), k):
                yield num
            return

        count = 0
        used_numbers = set()
        
        while True:
            if self.limit is not None and count >= self.limit:
                break
            
            if self.distinct and len(used_numbers) >= self._range_size:
                break
            
            num = self._generate_next(used_numbers)
            if num is None:
                break
            
            count += 1
            yield num
