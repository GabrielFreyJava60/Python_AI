import unittest
from MyArray import MyArray


class TestMyArray(unittest.TestCase):
    def setUp(self):
        self.array = MyArray[int](5)
    
    def test_constructor(self):
        self.assertEqual(self.array.amount, 5)
        array_large = MyArray[int](1000000000)
        self.assertEqual(array_large.amount, 1000000000)
    
    def test_constructor_negative(self):
        with self.assertRaises(ValueError):
            MyArray[int](-1)
    
    def test_set_get(self):
        self.array.set(0, 10)
        self.array.set(2, 20)
        self.assertEqual(self.array.get(0), 10)
        self.assertEqual(self.array.get(2), 20)
    
    def test_set_index_error(self):
        with self.assertRaises(IndexError):
            self.array.set(-1, 10)
        with self.assertRaises(IndexError):
            self.array.set(5, 10)
        with self.assertRaises(IndexError):
            self.array.set(10, 10)
    
    def test_get_index_error(self):
        with self.assertRaises(IndexError):
            self.array.get(-1)
        with self.assertRaises(IndexError):
            self.array.get(5)
        with self.assertRaises(IndexError):
            self.array.get(10)
    
    def test_setAll(self):
        self.array.setAll(42)
        for i in range(5):
            self.assertEqual(self.array.get(i), 42)
    
    def test_setAll_override(self):
        self.array.set(0, 10)
        self.array.set(1, 20)
        self.array.setAll(99)
        for i in range(5):
            self.assertEqual(self.array.get(i), 99)
    
    def test_set_after_setAll(self):
        self.array.setAll(50)
        self.array.set(2, 100)
        self.assertEqual(self.array.get(0), 50)
        self.assertEqual(self.array.get(1), 50)
        self.assertEqual(self.array.get(2), 100)
        self.assertEqual(self.array.get(3), 50)
        self.assertEqual(self.array.get(4), 50)
    
    def test_multiple_setAll(self):
        self.array.setAll(10)
        self.array.setAll(20)
        for i in range(5):
            self.assertEqual(self.array.get(i), 20)
    
    def test_large_array(self):
        large_array = MyArray[int](1000)
        large_array.setAll(999)
        self.assertEqual(large_array.get(0), 999)
        self.assertEqual(large_array.get(999), 999)
        large_array.set(500, 555)
        self.assertEqual(large_array.get(500), 555)
        self.assertEqual(large_array.get(501), 999)


if __name__ == '__main__':
    unittest.main()
