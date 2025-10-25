import unittest
from main import LfuDictCache


class TestLfuDictCache(unittest.TestCase):
    def setUp(self):
        self.cache = LfuDictCache(3)
    
    def test_put_and_get(self):
        self.cache.put(1, "a")
        self.cache.put(2, "b")
        self.assertEqual(self.cache.get(1), "a")
        self.assertEqual(self.cache.get(2), "b")
    
    def test_get_nonexistent(self):
        self.assertIsNone(self.cache.get(1))
    
    def test_capacity_exceeded(self):
        self.cache.put(1, "a")
        self.cache.put(2, "b")
        self.cache.put(3, "c")
        self.cache.put(4, "d")
        
        self.assertIsNone(self.cache.get(1))
        self.assertEqual(self.cache.get(2), "b")
        self.assertEqual(self.cache.get(3), "c")
        self.assertEqual(self.cache.get(4), "d")
    
    def test_lfu_eviction(self):
        self.cache.put(1, "a")
        self.cache.put(2, "b")
        self.cache.put(3, "c")
        
        self.cache.get(1)
        self.cache.get(1)
        self.cache.get(2)
        
        self.cache.put(4, "d")
        
        self.assertEqual(self.cache.get(1), "a")
        self.assertEqual(self.cache.get(2), "b")
        self.assertIsNone(self.cache.get(3))
        self.assertEqual(self.cache.get(4), "d")
    
    def test_lru_tie_breaking(self):
        self.cache.put(1, "a")
        self.cache.put(2, "b")
        self.cache.put(3, "c")
        
        self.cache.get(1)
        self.cache.get(2)
        self.cache.get(3)
        
        self.cache.put(4, "d")
        
        self.assertIsNone(self.cache.get(1))
        self.assertEqual(self.cache.get(2), "b")
        self.assertEqual(self.cache.get(3), "c")
        self.assertEqual(self.cache.get(4), "d")
    
    def test_update_existing_key(self):
        self.cache.put(1, "a")
        self.cache.put(1, "b")
        self.assertEqual(self.cache.get(1), "b")
    
    def test_zero_capacity(self):
        cache = LfuDictCache(0)
        cache.put(1, "a")
        self.assertIsNone(cache.get(1))
    
    def test_size(self):
        self.assertEqual(self.cache.size(), 0)
        self.cache.put(1, "a")
        self.assertEqual(self.cache.size(), 1)
        self.cache.put(2, "b")
        self.assertEqual(self.cache.size(), 2)
    
    def test_clear(self):
        self.cache.put(1, "a")
        self.cache.put(2, "b")
        self.cache.clear()
        self.assertEqual(self.cache.size(), 0)
        self.assertIsNone(self.cache.get(1))
        self.assertIsNone(self.cache.get(2))
    
    def test_complex_frequency_updates(self):
        self.cache.put(1, "a")
        self.cache.put(2, "b")
        self.cache.put(3, "c")
        
        self.cache.get(1)
        self.cache.get(1)
        self.cache.get(2)
        self.cache.get(3)
        self.cache.get(3)
        self.cache.get(3)
        
        self.cache.put(4, "d")
        
        self.assertEqual(self.cache.get(1), "a")
        self.assertIsNone(self.cache.get(2))
        self.assertEqual(self.cache.get(3), "c")
        self.assertEqual(self.cache.get(4), "d")
    
    def test_single_element(self):
        cache = LfuDictCache(1)
        cache.put(1, "a")
        self.assertEqual(cache.get(1), "a")
        cache.put(2, "b")
        self.assertIsNone(cache.get(1))
        self.assertEqual(cache.get(2), "b")


if __name__ == '__main__':
    unittest.main()
