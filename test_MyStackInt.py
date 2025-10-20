import unittest
from MyStackInt import MyStackInt


class TestMyStackInt(unittest.TestCase):
    def setUp(self):
        self.stack = MyStackInt()
    
    def test_push_pop(self):
        self.stack.push(5)
        self.assertEqual(self.stack.pop(), 5)
    
    def test_max(self):
        self.stack.push(3)
        self.stack.push(7)
        self.stack.push(2)
        self.assertEqual(self.stack.max(), 7)
    
    def test_empty_stack_error(self):
        with self.assertRaises(IndexError):
            self.stack.pop()
        with self.assertRaises(IndexError):
            self.stack.max()
    
    def test_multiple_operations(self):
        self.stack.push(1)
        self.stack.push(5)
        self.stack.push(3)
        self.assertEqual(self.stack.max(), 5)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.max(), 5)
        self.assertEqual(self.stack.pop(), 5)
        self.assertEqual(self.stack.max(), 1)


if __name__ == '__main__':
    unittest.main()