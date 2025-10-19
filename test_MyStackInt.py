import unittest
from MyStackInt import MyStackInt


class TestMyStackInt(unittest.TestCase):
    def setUp(self):
        self.stack = MyStackInt()
    
    def test_empty_stack_initialization(self):
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
    
    def test_push_single_element(self):
        self.stack.push(5)
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.max(), 5)
    
    def test_push_multiple_elements(self):
        elements = [3, 7, 2, 9, 1]
        for element in elements:
            self.stack.push(element)
        
        self.assertEqual(self.stack.size(), 5)
        self.assertEqual(self.stack.max(), 9)
    
    def test_pop_single_element(self):
        self.stack.push(42)
        result = self.stack.pop()
        self.assertEqual(result, 42)
        self.assertTrue(self.stack.is_empty())
    
    def test_pop_multiple_elements(self):
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            self.stack.push(element)
        
        for i in range(len(elements) - 1, -1, -1):
            self.assertEqual(self.stack.pop(), elements[i])
        
        self.assertTrue(self.stack.is_empty())
    
    def test_max_with_ascending_elements(self):
        elements = [1, 2, 3, 4, 5]
        for i, element in enumerate(elements):
            self.stack.push(element)
            self.assertEqual(self.stack.max(), element)
    
    def test_max_with_descending_elements(self):
        elements = [5, 4, 3, 2, 1]
        for element in elements:
            self.stack.push(element)
            self.assertEqual(self.stack.max(), 5)
    
    def test_max_with_mixed_elements(self):
        test_cases = [
            ([3, 1, 4, 1, 5], [3, 3, 4, 4, 5]),
            ([5, 2, 8, 1, 3], [5, 5, 8, 8, 8]),
            ([1, 1, 1, 1, 1], [1, 1, 1, 1, 1]),
            ([10, 5, 15, 3, 20], [10, 10, 15, 15, 20])
        ]
        
        for elements, expected_maxes in test_cases:
            stack = MyStackInt()
            for element, expected_max in zip(elements, expected_maxes):
                stack.push(element)
                self.assertEqual(stack.max(), expected_max)
    
    def test_max_after_pop(self):
        elements = [1, 5, 3, 9, 2]
        for element in elements:
            self.stack.push(element)
        
        expected_maxes = [9, 9, 5, 5, 1]
        
        for i in range(len(elements)):
            self.assertEqual(self.stack.max(), expected_maxes[i])
            self.stack.pop()
        
        self.assertTrue(self.stack.is_empty())
    
    def test_pop_from_empty_stack_raises_error(self):
        with self.assertRaises(IndexError) as context:
            self.stack.pop()
        self.assertEqual(str(context.exception), "pop from empty stack")
    
    def test_max_from_empty_stack_raises_error(self):
        with self.assertRaises(IndexError) as context:
            self.stack.max()
        self.assertEqual(str(context.exception), "max from empty stack")
    
    def test_complex_sequence(self):
        self.stack.push(10)
        self.stack.push(5)
        self.stack.push(15)
        self.assertEqual(self.stack.max(), 15)
        
        self.assertEqual(self.stack.pop(), 15)
        self.assertEqual(self.stack.max(), 10)
        
        self.stack.push(20)
        self.stack.push(3)
        self.assertEqual(self.stack.max(), 20)
        
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 20)
        self.assertEqual(self.stack.max(), 10)
        
        self.assertEqual(self.stack.pop(), 5)
        self.assertEqual(self.stack.max(), 10)
        self.assertEqual(self.stack.pop(), 10)
        
        self.assertTrue(self.stack.is_empty())
    
    def test_duplicate_maximums(self):
        elements = [5, 3, 5, 1, 5]
        for element in elements:
            self.stack.push(element)
        
        self.assertEqual(self.stack.max(), 5)
        
        self.assertEqual(self.stack.pop(), 5)
        self.assertEqual(self.stack.max(), 5)
        
        self.assertEqual(self.stack.pop(), 1)
        self.assertEqual(self.stack.max(), 5)
        
        self.assertEqual(self.stack.pop(), 5)
        self.assertEqual(self.stack.max(), 5)
        
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.max(), 5)
        
        self.assertEqual(self.stack.pop(), 5)
        self.assertTrue(self.stack.is_empty())
    
    def test_negative_numbers(self):
        elements = [-5, -1, -10, -3]
        for element in elements:
            self.stack.push(element)
        
        self.assertEqual(self.stack.max(), -1)
        
        self.assertEqual(self.stack.pop(), -3)
        self.assertEqual(self.stack.max(), -1)
        
        self.assertEqual(self.stack.pop(), -10)
        self.assertEqual(self.stack.max(), -1)
        
        self.assertEqual(self.stack.pop(), -1)
        self.assertEqual(self.stack.max(), -5)
        
        self.assertEqual(self.stack.pop(), -5)
        self.assertTrue(self.stack.is_empty())
    
    def test_zero_and_positive_numbers(self):
        elements = [0, 5, 0, 10, 0]
        for element in elements:
            self.stack.push(element)
        
        self.assertEqual(self.stack.max(), 10)
        
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
    unittest.main(verbosity=2)