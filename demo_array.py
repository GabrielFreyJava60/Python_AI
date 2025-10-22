from MyArray import MyArray

print("=== MyArray Demonstration ===")

array = MyArray[int](5)
print(f"Created array with {array.amount} elements")

print("\nSetting individual values:")
array.set(0, 10)
array.set(2, 20)
array.set(4, 30)
print(f"array[0] = {array.get(0)}")
print(f"array[2] = {array.get(2)}")
print(f"array[4] = {array.get(4)}")

print("\nUsing setAll:")
array.setAll(99)
for i in range(5):
    print(f"array[{i}] = {array.get(i)}")

print("\nSetting value after setAll:")
array.set(1, 77)
for i in range(5):
    print(f"array[{i}] = {array.get(i)}")

print("\nLarge array test:")
large_array = MyArray[int](1000000)
print(f"Created array with {large_array.amount:,} elements")
large_array.setAll(42)
print(f"Set all to 42, array[0] = {large_array.get(0)}")
print(f"array[999999] = {large_array.get(999999)}")

print("\nError handling:")
try:
    array.set(-1, 10)
except IndexError as e:
    print(f"Error: {e}")

try:
    array.get(10)
except IndexError as e:
    print(f"Error: {e}")
