from main import RandomNumbersStream

print("=== RandomNumbersStream Demonstration ===\n")

print("1. Endless Random Numbers Streaming:")
print("   (Limited to 5 numbers for demo)")
numbers1 = RandomNumbersStream(min=10, max=100)
count = 0
for num in numbers1:
    print(f"   {num}")
    count += 1
    if count >= 5:  # Break after 5 for demo purposes
        break

print("\n2. Endless Even Random Numbers Streaming:")
print("   (Limited to 5 numbers for demo)")
numbers2 = RandomNumbersStream(min=10, max=100)
numbers2.setFilter(lambda n: n % 2 == 0)
count = 0
for num in numbers2:
    print(f"   {num}")
    count += 1
    if count >= 5:  # Break after 5 for demo purposes
        break

print("\n3. Limited Even Random Numbers Streaming:")
numbers3 = RandomNumbersStream(min=10, max=100)
numbers3.setFilter(lambda n: n % 2 == 0)
numbers3.setLimit(10)
print("   First 10 even numbers:")
for num in numbers3:
    print(f"   {num}")

print("\n4. Sport Lotto (Unique Random Numbers):")
numbers4 = RandomNumbersStream(min=1, max=49)
numbers4.setDistinct()
numbers4.setLimit(10)
print("   10 unique random numbers in [1, 49]:")
for num in numbers4:
    print(f"   {num}")

print("\n5. Testing resetDistinct and multiple iterations:")
numbers5 = RandomNumbersStream(min=1, max=5)
numbers5.setDistinct()
numbers5.setLimit(5)
print("   Distinct mode (should get all 5 numbers):")
result1 = []
for num in numbers5:
    result1.append(num)
    print(f"   {num}", end=" ")
print(f"\n   Generated {len(result1)} numbers, all unique: {len(set(result1)) == len(result1)}")

numbers5.resetDistinct()
numbers5.setLimit(10)
print("\n   After resetDistinct (may repeat):")
result2 = []
for num in numbers5:
    result2.append(num)
    print(f"   {num}", end=" ")
print(f"\n   Generated {len(result2)} numbers, has repeats: {len(set(result2)) < len(result2)}")
