import unittest
from MyArray import MyArray


class TestMyArray(unittest.TestCase):
    def setUp(self):
        self.array = MyArray[int](5)
    
    def test_constructor(self):
        self.assertEqual(self.array.getSize(), 5)
        array_large = MyArray[int](1000000000)
        self.assertEqual(array_large.getSize(), 1000000000)
    
    def test_constructor_negative(self):
        with self.assertRaises(ValueError):
            MyArray[int](-1)
    
    def test_constructor_zero(self):
        array_zero = MyArray[int](0)
        self.assertEqual(array_zero.getSize(), 0)
        with self.assertRaises(IndexError):
            array_zero.get(0)
    
    def test_set_get_basic(self):
        self.array.set(0, 10)
        self.array.set(2, 20)
        self.assertEqual(self.array.get(0), 10)
        self.assertEqual(self.array.get(2), 20)
    
    def test_set_get_boundary_indices(self):
        self.array.set(0, 100)
        self.array.set(4, 400)
        self.assertEqual(self.array.get(0), 100)
        self.assertEqual(self.array.get(4), 400)
    
    def test_set_index_error_negative(self):
        with self.assertRaises(IndexError) as context:
            self.array.set(-1, 10)
        self.assertIn("Index -1 out of range", str(context.exception))
    
    def test_set_index_error_too_large(self):
        with self.assertRaises(IndexError) as context:
            self.array.set(5, 10)
        self.assertIn("Index 5 out of range", str(context.exception))
    
    def test_set_index_error_boundary(self):
        with self.assertRaises(IndexError):
            self.array.set(5, 10)
    
    def test_get_index_error_negative(self):
        with self.assertRaises(IndexError) as context:
            self.array.get(-1)
        self.assertIn("Index -1 out of range", str(context.exception))
    
    def test_get_index_error_too_large(self):
        with self.assertRaises(IndexError) as context:
            self.array.get(5)
        self.assertIn("Index 5 out of range", str(context.exception))
    
    def test_setAll_basic(self):
        self.array.setAll(42)
        for i in range(5):
            self.assertEqual(self.array.get(i), 42)
    
    def test_setAll_after_individual_sets(self):
        self.array.set(0, 10)
        self.array.set(1, 20)
        self.array.set(2, 30)
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
    
    def test_setAll_then_set_then_setAll(self):
        self.array.setAll(100)
        self.array.set(1, 200)
        self.array.set(3, 300)
        self.assertEqual(self.array.get(0), 100)
        self.assertEqual(self.array.get(1), 200)
        self.assertEqual(self.array.get(3), 300)
        
        self.array.setAll(500)
        for i in range(5):
            self.assertEqual(self.array.get(i), 500)
    
    def test_large_array_memory_efficiency(self):
        large_array = MyArray[int](1000000)
        large_array.setAll(999)
        self.assertEqual(large_array.get(0), 999)
        self.assertEqual(large_array.get(999999), 999)
        large_array.set(500000, 555)
        self.assertEqual(large_array.get(500000), 555)
        self.assertEqual(large_array.get(500001), 999)
        self.assertEqual(large_array.get(0), 999)
    
    def test_huge_array(self):
        huge_array = MyArray[int](1000000000)
        huge_array.setAll(42)
        self.assertEqual(huge_array.get(0), 42)
        self.assertEqual(huge_array.get(999999999), 42)
        huge_array.set(500000000, 100)
        self.assertEqual(huge_array.get(500000000), 100)
        self.assertEqual(huge_array.get(500000001), 42)
    
    def test_uninitialized_value_error(self):
        array = MyArray[int](3)
        with self.assertRaises(ValueError) as context:
            array.get(0)
        self.assertIn("No value set at index 0", str(context.exception))
    
    def test_mixed_operations(self):
        self.array.setAll(100)
        self.array.set(1, 200)
        self.array.set(3, 300)
        self.array.setAll(500)
        self.array.set(2, 600)
        
        expected = [500, 500, 600, 500, 500]
        for i, exp in enumerate(expected):
            self.assertEqual(self.array.get(i), exp)
    
    def test_getSize(self):
        self.assertEqual(self.array.getSize(), 5)
        array_10 = MyArray[int](10)
        self.assertEqual(array_10.getSize(), 10)
        array_0 = MyArray[int](0)
        self.assertEqual(array_0.getSize(), 0)


if __name__ == '__main__':
    unittest.main()
