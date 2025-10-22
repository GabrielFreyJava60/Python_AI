from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class MyArray(Generic[T]):
    def __init__(self, amount: int):
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        self._size = amount
        self._overrides = {}
        self._default_value: Optional[T] = None
        self._has_default = False
    
    def setAll(self, value: T) -> None:
        self._default_value = value
        self._has_default = True
        self._overrides.clear()
    
    def set(self, index: int, value: T) -> None:
        if not (0 <= index < self._size):
            raise IndexError(f"Index {index} out of range [0, {self._size})")
        self._overrides[index] = value
    
    def get(self, index: int) -> T:
        if not (0 <= index < self._size):
            raise IndexError(f"Index {index} out of range [0, {self._size})")
        
        if index in self._overrides:
            return self._overrides[index]
        
        if self._has_default:
            return self._default_value
        
        raise ValueError(f"No value set at index {index}. Call setAll() or set() first.")
    
    def getSize(self) -> int:
        return self._size
