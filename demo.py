#!/usr/bin/env python3
"""
Demonstration script for MyStackInt class.
Shows basic usage and O(1) complexity operations.
"""

from MyStackInt import MyStackInt


def main():
    """Demonstrate MyStackInt functionality."""
    print("=== MyStackInt Demonstration ===\n")
    
    # Create a new stack
    stack = MyStackInt()
    print(f"Created empty stack: {stack}")
    print(f"Is empty: {stack.is_empty()}")
    print(f"Size: {stack.size()}\n")
    
    # Push some elements
    elements = [5, 3, 8, 2, 9, 1]
    print("Pushing elements:", elements)
    
    for element in elements:
        stack.push(element)
        print(f"Pushed {element}, max: {stack.max()}, size: {stack.size()}")
    
    print(f"\nStack after pushing all elements: {stack}")
    print(f"Current max: {stack.max()}\n")
    
    # Demonstrate pop operations
    print("Popping elements (LIFO order):")
    while not stack.is_empty():
        popped = stack.pop()
        max_val = stack.max() if not stack.is_empty() else "N/A (empty)"
        print(f"Popped {popped}, remaining max: {max_val}, size: {stack.size()}")
    
    print(f"\nStack after popping all elements: {stack}")
    print(f"Is empty: {stack.is_empty()}")
    
    # Demonstrate error handling
    print("\n=== Error Handling ===")
    try:
        stack.pop()
    except IndexError as e:
        print(f"pop() on empty stack: {e}")
    
    try:
        stack.max()
    except IndexError as e:
        print(f"max() on empty stack: {e}")
    
    # Demonstrate with negative numbers
    print("\n=== Working with Negative Numbers ===")
    negative_stack = MyStackInt()
    negative_elements = [-5, -1, -10, -3, -2]
    
    for element in negative_elements:
        negative_stack.push(element)
        print(f"Pushed {element}, max: {negative_stack.max()}")
    
    print(f"Final max: {negative_stack.max()}")
    
    # Demonstrate duplicate maximums
    print("\n=== Duplicate Maximums ===")
    duplicate_stack = MyStackInt()
    duplicate_elements = [3, 5, 2, 5, 1, 5]
    
    for element in duplicate_elements:
        duplicate_stack.push(element)
        print(f"Pushed {element}, max: {duplicate_stack.max()}")
    
    print("\nPopping with duplicate maximums:")
    while not duplicate_stack.is_empty():
        popped = duplicate_stack.pop()
        max_val = duplicate_stack.max() if not duplicate_stack.is_empty() else "N/A (empty)"
        print(f"Popped {popped}, remaining max: {max_val}")


if __name__ == "__main__":
    main()
