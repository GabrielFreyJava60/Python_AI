import unittest
from MyStackInt import MyStackInt


class TestMyStackInt(unittest.TestCase):
    """Test cases for MyStackInt class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.stack = MyStackInt()
    
    def test_empty_stack_initialization(self):
        """Test that a new stack is empty."""
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
    
    def test_push_single_element(self):
        """Test pushing a single element."""
        self.stack.push(5)
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.max(), 5)
    
    def test_push_multiple_elements(self):
        """Test pushing multiple elements."""
        elements = [3, 7, 2, 9, 1]
        for element in elements:
            self.stack.push(element)
        
        self.assertEqual(self.stack.size(), 5)
        self.assertEqual(self.stack.max(), 9)
    
    def test_pop_single_element(self):
        """Test popping a single element."""
        self.stack.push(42)
        result = self.stack.pop()
        self.assertEqual(result, 42)
        self.assertTrue(self.stack.is_empty())
    
    def test_pop_multiple_elements(self):
        """Test popping multiple elements in LIFO order."""
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            self.stack.push(element)
        
        # Pop in reverse order
        for i in range(len(elements) - 1, -1, -1):
            self.assertEqual(self.stack.pop(), elements[i])
        
        self.assertTrue(self.stack.is_empty())
    
    def test_max_with_ascending_elements(self):
        """Test max with elements in ascending order."""
        elements = [1, 2, 3, 4, 5]
        for i, element in enumerate(elements):
            self.stack.push(element)
            self.assertEqual(self.stack.max(), element)  # Max should be the last element
    
    def test_max_with_descending_elements(self):
        """Test max with elements in descending order."""
        elements = [5, 4, 3, 2, 1]
        for element in elements:
            self.stack.push(element)
            self.assertEqual(self.stack.max(), 5)  # Max should always be 5
    
    def test_max_with_mixed_elements(self):
        """Test max with mixed order elements."""
        test_cases = [
            ([3, 1, 4, 1, 5], [3, 3, 4, 4, 5]),  # (elements, expected_maxes)
            ([5, 2, 8, 1, 3], [5, 5, 8, 8, 8]),
            ([1, 1, 1, 1, 1], [1, 1, 1, 1, 1]),  # All same elements
            ([10, 5, 15, 3, 20], [10, 10, 15, 15, 20])
        ]
        
        for elements, expected_maxes in test_cases:
            stack = MyStackInt()
            for element, expected_max in zip(elements, expected_maxes):
                stack.push(element)
                self.assertEqual(stack.max(), expected_max)
    
    def test_max_after_pop(self):
        """Test that max updates correctly after popping elements."""
        elements = [1, 5, 3, 9, 2]
        for element in elements:
            self.stack.push(element)
        
        # Expected maxes after each pop (check before popping)
        expected_maxes = [9, 9, 5, 5, 1]  # Max before each pop
        
        for i in range(len(elements)):
            self.assertEqual(self.stack.max(), expected_maxes[i])
            self.stack.pop()
        
        # Stack should be empty now
        self.assertTrue(self.stack.is_empty())
    
    def test_pop_from_empty_stack_raises_error(self):
        """Test that popping from empty stack raises IndexError."""
        with self.assertRaises(IndexError) as context:
            self.stack.pop()
        self.assertEqual(str(context.exception), "pop from empty stack")
    
    def test_max_from_empty_stack_raises_error(self):
        """Test that getting max from empty stack raises IndexError."""
        with self.assertRaises(IndexError) as context:
            self.stack.max()
        self.assertEqual(str(context.exception), "max from empty stack")
    
    def test_complex_sequence(self):
        """Test a complex sequence of operations."""
        # Push some elements
        self.stack.push(10)
        self.stack.push(5)
        self.stack.push(15)
        self.assertEqual(self.stack.max(), 15)
        
        # Pop and check max
        self.assertEqual(self.stack.pop(), 15)
        self.assertEqual(self.stack.max(), 10)
        
        # Push more elements
        self.stack.push(20)
        self.stack.push(3)
        self.assertEqual(self.stack.max(), 20)
        
        # Pop multiple elements
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 20)
        self.assertEqual(self.stack.max(), 10)
        
        # Final pop
        self.assertEqual(self.stack.pop(), 5)
        self.assertEqual(self.stack.max(), 10)
        self.assertEqual(self.stack.pop(), 10)
        
        # Stack should be empty
        self.assertTrue(self.stack.is_empty())
    
    def test_duplicate_maximums(self):
        """Test behavior with duplicate maximum values."""
        elements = [5, 3, 5, 1, 5]
        for element in elements:
            self.stack.push(element)
        
        # Max should be 5 throughout
        self.assertEqual(self.stack.max(), 5)
        
        # Pop elements and check max updates correctly
        self.assertEqual(self.stack.pop(), 5)  # Remove last 5
        self.assertEqual(self.stack.max(), 5)  # Max should still be 5
        
        self.assertEqual(self.stack.pop(), 1)
        self.assertEqual(self.stack.max(), 5)  # Max should still be 5
        
        self.assertEqual(self.stack.pop(), 5)  # Remove second 5
        self.assertEqual(self.stack.max(), 5)  # Max should still be 5
        
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.max(), 5)  # Max should still be 5
        
        self.assertEqual(self.stack.pop(), 5)  # Remove first 5
        self.assertTrue(self.stack.is_empty())
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        elements = [-5, -1, -10, -3]
        for element in elements:
            self.stack.push(element)
        
        self.assertEqual(self.stack.max(), -1)  # -1 is the maximum
        
        self.assertEqual(self.stack.pop(), -3)
        self.assertEqual(self.stack.max(), -1)
        
        self.assertEqual(self.stack.pop(), -10)
        self.assertEqual(self.stack.max(), -1)
        
        self.assertEqual(self.stack.pop(), -1)
        self.assertEqual(self.stack.max(), -5)
        
        self.assertEqual(self.stack.pop(), -5)
        self.assertTrue(self.stack.is_empty())
    
    def test_zero_and_positive_numbers(self):
        """Test with zero and positive numbers."""
        elements = [0, 5, 0, 10, 0]
        for element in elements:
            self.stack.push(element)
        
        self.assertEqual(self.stack.max(), 10)
        
        # Pop and verify max updates
        self.assertEqual(self.stack.pop(), 0)
        self.assertEqual(self.stack.max(), 10)
        
        self.assertEqual(self.stack.pop(), 10)
        self.assertEqual(self.stack.max(), 5)
        
        self.assertEqual(self.stack.pop(), 0)
        self.assertEqual(self.stack.max(), 5)
        
        self.assertEqual(self.stack.pop(), 5)
        self.assertEqual(self.stack.max(), 0)
        
        self.assertEqual(self.stack.pop(), 0)
        self.assertTrue(self.stack.is_empty())
    
    def test_string_representation(self):
        """Test string representation methods."""
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        
        str_repr = str(self.stack)
        self.assertIn("MyStackInt", str_repr)
        self.assertIn("[1, 2, 3]", str_repr)
        
        repr_str = repr(self.stack)
        self.assertIn("MyStackInt", repr_str)
        self.assertIn("stack=", repr_str)
        self.assertIn("max_stack=", repr_str)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
