class MyStackInt:
    def __init__(self):
        self._stack = []
        self._max_stack = []
    
    def push(self, num: int) -> None:
        self._stack.append(num)
        if not self._max_stack or num >= self._max_stack[-1]:
            self._max_stack.append(num)
    
    def pop(self) -> int:
        if not self._stack:
            raise IndexError("pop from empty stack")
        num = self._stack.pop()
        if self._max_stack and num == self._max_stack[-1]:
            self._max_stack.pop()
        return num
    
    def max(self) -> int:
        if not self._stack:
            raise IndexError("max from empty stack")
        return self._max_stack[-1]
    
    def is_empty(self) -> bool:
        return len(self._stack) == 0
    
    def size(self) -> int:
        return len(self._stack)
    
    def __str__(self) -> str:
        return f"MyStackInt({self._stack})"
    
    def __repr__(self) -> str:
        return f"MyStackInt(stack={self._stack}, max_stack={self._max_stack})"
