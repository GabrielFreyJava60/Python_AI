# HW #25 Definition

## Write class MyStackInt with the following methods
- push(num: int) adds number at top of the stack
- pop()->int removes number from the top of stack with returning the number. Raises IndexError for empty stack
- max()->int retuns maximal number in the stack. Raises IndexError for empty stack

## Note all the above mathods should have complexity O[1]

## Write tests for class MyStackInt

# HW #26 Definition

## Write generic class MyArray[T] with the following methods
- constructor taking amount of items (It may be very huge for example 1000000000)
- setAll - sets in all items the same given value
- set - sets a given value at a given index (index may be ether 0 or any positive number less than amount of items), raises IndexError exception if the index greater or equal the amount or less than 0
- get - returns the value at a given index (index may be ether 0 or any positive number less than amount of items), raises IndexError exception if the index greater or equal the amount or less than 0

## Note all the above mathods should have complexity O[1]

## Write tests for class MyArray[int]

## Files
- `MyStackInt.py` - implementation of MyStackInt class
- `test_MyStackInt.py` - tests for MyStackInt class
- `demo.py` - demonstration script for MyStackInt
- `MyArray.py` - implementation of MyArray[T] class
- `test_MyArray.py` - tests for MyArray[int] class
- `demo_array.py` - demonstration script for MyArray