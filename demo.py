from MyStackInt import MyStackInt

stack = MyStackInt()

print("Push 5, 3, 8")
stack.push(5)
stack.push(3)
stack.push(8)

print(f"Max: {stack.max()}")
print(f"Pop: {stack.pop()}")
print(f"Max: {stack.max()}")
print(f"Pop: {stack.pop()}")
print(f"Max: {stack.max()}")
print(f"Pop: {stack.pop()}")

try:
    stack.pop()
except IndexError as e:
    print(f"Error: {e}")