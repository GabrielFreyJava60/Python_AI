from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class MyArray(Generic[T]):
    def __init__(self, amount: int):
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        self.amount = amount
        self.data = {}
        self.global_value: Optional[T] = None
        self.global_set = False
    
    def setAll(self, value: T) -> None:
        self.global_value = value
        self.global_set = True
        self.data.clear()
    
    def set(self, index: int, value: T) -> None:
        if index < 0 or index >= self.amount:
            raise IndexError("Index out of range")
        self.data[index] = value
    
    def get(self, index: int) -> T:
        if index < 0 or index >= self.amount:
            raise IndexError("Index out of range")
        if self.global_set and index not in self.data:
            return self.global_value
        return self.data.get(index, self.global_value)
