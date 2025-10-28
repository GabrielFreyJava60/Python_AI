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
        self._generated_numbers: set[int] = set()
    
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
        self._generated_numbers.clear()
    
    def _passes_filter(self, num: int) -> bool:
        if self.filter_predicate is None:
            return True
        try:
            return self.filter_predicate(num)
        except Exception:
            return False
    
    def _generate_next(self) -> Optional[int]:
        max_possible = self.max - self.min + 1
        max_attempts = max(10000, max_possible * 10)
        
        for _ in range(max_attempts):
            num = random.randint(self.min, self.max)
            
            if self.distinct and num in self._generated_numbers:
                continue
            
            if not self._passes_filter(num):
                continue
            
            if self.distinct:
                self._generated_numbers.add(num)
            return num
        
        return None
    
    def __iter__(self) -> Iterator[int]:
        count = 0
        if self.distinct:
            self._generated_numbers.clear()
        
        max_possible = self.max - self.min + 1
        
        while True:
            if self.limit is not None and count >= self.limit:
                break
            
            if self.distinct and len(self._generated_numbers) >= max_possible:
                break
            
            num = self._generate_next()
            if num is None:
                break
            
            count += 1
            yield num
