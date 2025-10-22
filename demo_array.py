from MyArray import MyArray

print("=== MyArray[T] Demonstration ===")
print("Generic array with O(1) operations and memory optimization\n")

array = MyArray[int](5)
print(f"Created array with {array.getSize()} elements")

print("\n1. Setting individual values:")
array.set(0, 10)
array.set(2, 20)
array.set(4, 30)
print(f"array[0] = {array.get(0)}")
print(f"array[2] = {array.get(2)}")
print(f"array[4] = {array.get(4)}")

print("\n2. Using setAll:")
array.setAll(99)
for i in range(5):
    print(f"array[{i}] = {array.get(i)}")

print("\n3. Setting value after setAll:")
array.set(1, 77)
for i in range(5):
    print(f"array[{i}] = {array.get(i)}")

print("\n4. Memory efficiency test:")
large_array = MyArray[int](1000000)
print(f"Created array with {large_array.getSize():,} elements")
large_array.setAll(42)
print(f"Set all to 42, array[0] = {large_array.get(0)}")
print(f"array[999999] = {large_array.get(999999)}")
large_array.set(500000, 555)
print(f"Set array[500000] = 555, array[500000] = {large_array.get(500000)}")
print(f"array[500001] still = {large_array.get(500001)}")

print("\n5. Huge array test:")
huge_array = MyArray[int](1000000000)
print(f"Created array with {huge_array.getSize():,} elements")
huge_array.setAll(100)
print(f"Set all to 100, array[0] = {huge_array.get(0)}")
print(f"array[999999999] = {huge_array.get(999999999)}")

print("\n6. Error handling:")
try:
    array.set(-1, 10)
except IndexError as e:
    print(f"set(-1, 10): {e}")

try:
    array.get(10)
except IndexError as e:
    print(f"get(10): {e}")

try:
    uninitialized = MyArray[int](3)
    uninitialized.get(0)
except ValueError as e:
    print(f"get() without setAll/set: {e}")

print("\n7. Mixed operations:")
array.setAll(100)
array.set(1, 200)
array.set(3, 300)
array.setAll(500)
array.set(2, 600)
print("setAll(100) -> set(1,200) -> set(3,300) -> setAll(500) -> set(2,600)")
for i in range(5):
    print(f"array[{i}] = {array.get(i)}")
