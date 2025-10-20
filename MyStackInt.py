class MyStackInt:
    def __init__(self):
        self.stack = []
        self.max_stack = []
    
    def push(self, num):
        self.stack.append(num)
        if not self.max_stack or num >= self.max_stack[-1]:
            self.max_stack.append(num)
    
    def pop(self):
        if not self.stack:
            raise IndexError("pop from empty stack")
        num = self.stack.pop()
        if self.max_stack and num == self.max_stack[-1]:
            self.max_stack.pop()
        return num
    
    def max(self):
        if not self.stack:
            raise IndexError("max from empty stack")
        return self.max_stack[-1]