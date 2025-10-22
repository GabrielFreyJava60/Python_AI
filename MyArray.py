from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class MyArray(Generic[T]):
    def __init__(self, amount: int):
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        self.amount = amount
        self._overrides = {}
        self._default_value: Optional[T] = None
    
    def setAll(self, value: T) -> None:
        self._default_value = value
        self._overrides.clear()
    
    def set(self, index: int, value: T) -> None:
        if index < 0 or index >= self.amount:
            raise IndexError("Index out of range")
        self._overrides[index] = value
    
    def get(self, index: int) -> T:
        if index < 0 or index >= self.amount:
            raise IndexError("Index out of range")
        if index in self._overrides:
            return self._overrides[index]
        if self._default_value is not None:
            return self._default_value
        raise ValueError("Value at index is not set")
