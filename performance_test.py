#!/usr/bin/env python3
"""
Performance test to demonstrate O(1) complexity of MyStackInt operations.
"""

import time
from MyStackInt import MyStackInt


def time_operation(operation, *args):
    """Time a single operation."""
    start_time = time.perf_counter()
    result = operation(*args)
    end_time = time.perf_counter()
    return result, end_time - start_time


def test_performance():
    """Test performance with different stack sizes."""
    print("=== Performance Test for MyStackInt ===\n")
    
    # Test different stack sizes
    sizes = [1000, 5000, 10000, 50000, 100000]
    
    for size in sizes:
        print(f"Testing with {size:,} elements:")
        
        # Create stack and fill it
        stack = MyStackInt()
        
        # Time push operations
        start_time = time.perf_counter()
        for i in range(size):
            stack.push(i)
        push_time = time.perf_counter() - start_time
        
        # Time max operations
        start_time = time.perf_counter()
        for _ in range(100):  # Test max 100 times
            stack.max()
        max_time = time.perf_counter() - start_time
        
        # Time pop operations
        start_time = time.perf_counter()
        for _ in range(size):
            stack.pop()
        pop_time = time.perf_counter() - start_time
        
        # Calculate average times
        avg_push_time = push_time / size
        avg_max_time = max_time / 100
        avg_pop_time = pop_time / size
        
        print(f"  Average push time: {avg_push_time:.8f} seconds")
        print(f"  Average max time:  {avg_max_time:.8f} seconds")
        print(f"  Average pop time:  {avg_pop_time:.8f} seconds")
        print(f"  Total time:        {push_time + max_time + pop_time:.4f} seconds")
        print()


def test_constant_time_complexity():
    """Test that operations maintain constant time complexity."""
    print("=== Constant Time Complexity Test ===\n")
    
    # Test with increasing sizes to verify O(1) behavior
    sizes = [1000, 2000, 4000, 8000, 16000]
    push_times = []
    max_times = []
    pop_times = []
    
    for size in sizes:
        stack = MyStackInt()
        
        # Time push operations
        start_time = time.perf_counter()
        for i in range(size):
            stack.push(i)
        push_time = time.perf_counter() - start_time
        push_times.append(push_time / size)
        
        # Time max operations
        start_time = time.perf_counter()
        for _ in range(100):
            stack.max()
        max_time = time.perf_counter() - start_time
        max_times.append(max_time / 100)
        
        # Time pop operations
        start_time = time.perf_counter()
        for _ in range(size):
            stack.pop()
        pop_time = time.perf_counter() - start_time
        pop_times.append(pop_time / size)
    
    print("Average operation times (should be relatively constant):")
    print("Size\t\tPush\t\tMax\t\tPop")
    print("-" * 50)
    
    for i, size in enumerate(sizes):
        print(f"{size:>6,}\t{push_times[i]:.8f}\t{max_times[i]:.8f}\t{pop_times[i]:.8f}")
    
    # Check if times are relatively constant (within reasonable variance)
    push_variance = max(push_times) / min(push_times) if min(push_times) > 0 else 1
    max_variance = max(max_times) / min(max_times) if min(max_times) > 0 else 1
    pop_variance = max(pop_times) / min(pop_times) if min(pop_times) > 0 else 1
    
    print(f"\nVariance ratios (should be close to 1.0 for O(1) complexity):")
    print(f"Push variance: {push_variance:.2f}")
    print(f"Max variance:  {max_variance:.2f}")
    print(f"Pop variance:  {pop_variance:.2f}")


if __name__ == "__main__":
    test_performance()
    test_constant_time_complexity()
