# HW #26 Definition

## Write generic class MyArray[T] with the following methods
- constructor taking amount of items (It may be very huge for example 1000000000)
- setAll - sets in all items the same given value
- set - sets a given value at a given index (index may be ether 0 or any positive number less than amount of items), raises IndexError exception if the index greater or equal the amount or less than 0
- get - returns the value at a given index (index may be ether 0 or any positive number less than amount of items), raises IndexError exception if the index greater or equal the amount or less than 0

## Note all the above mathods should have complexity O[1]

## Write tests for class MyArray[int]

## Implementation Details

### Memory Optimization
Instead of storing all elements in memory, MyArray uses an optimized approach:
- **Default value**: Set by `setAll()` operation
- **Individual overrides**: Dictionary storing only modified elements
- **O(1) operations**: All methods run in constant time regardless of array size

### Key Features
- ✅ **O(1) complexity** for all operations (set, get, setAll)
- ✅ **Memory efficient** - handles arrays up to 1 billion elements
- ✅ **Generic support** - works with any type T
- ✅ **Proper error handling** - IndexError for invalid indices, ValueError for uninitialized values
- ✅ **Comprehensive testing** - 18 test cases covering all scenarios

### Algorithm
1. **setAll(value)**: Sets default value and clears individual overrides - O(1)
2. **set(index, value)**: Stores value in overrides dictionary - O(1)
3. **get(index)**: Returns override if exists, otherwise default value - O(1)

### Memory Usage Example
For array of 1,000,000,000 elements:
- **Traditional approach**: ~8GB memory (1B × 8 bytes)
- **MyArray approach**: ~8 bytes + overrides (only modified elements)

## Files
- `MyArray.py` - implementation of MyArray[T] class with full documentation
- `test_MyArray.py` - comprehensive test suite (18 tests)
- `demo_array.py` - demonstration script showing all features