"""
Tests for ImageInfo class.
"""
import unittest
import os
import pandas as pd
from pathlib import Path
from image_info import ImageInfo


class TestImageInfo(unittest.TestCase):
    """Test cases for ImageInfo class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        # Use a test image - you can replace this with any image path
        # For testing, we'll check if street.jpg exists, otherwise use any available image
        test_image_paths = [
            "street.jpg",
            "../street.jpg",
            "test_image.jpg"
        ]
        
        cls.test_image = None
        for path in test_image_paths:
            if Path(path).exists():
                cls.test_image = path
                break
        
        if cls.test_image is None:
            # Try to find any image file in current directory
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            for ext in image_extensions:
                images = list(Path('.').glob(f'*{ext}'))
                if images:
                    cls.test_image = str(images[0])
                    break
        
        if cls.test_image is None:
            raise FileNotFoundError(
                "No test image found. Please provide an image file for testing."
            )
    
    def setUp(self):
        """Set up before each test."""
        if self.test_image:
            self.image_info = ImageInfo(self.test_image)
    
    def test_initialization(self):
        """Test ImageInfo initialization."""
        self.assertIsNotNone(self.image_info)
        self.assertIsNotNone(self.image_info.model)
        self.assertIsNotNone(self.image_info.results)
        self.assertGreater(self.image_info.image_width, 0)
        self.assertGreater(self.image_info.image_height, 0)
    
    def test_boxesClass(self):
        """Test boxesClass method."""
        # Test with a common class (person is usually present in street scenes)
        person_indices = self.image_info.boxesClass("person")
        self.assertIsInstance(person_indices, list)
        
        # Test with a class that might not exist
        airplane_indices = self.image_info.boxesClass("airplane")
        self.assertIsInstance(airplane_indices, list)
    
    def test_boxInfo(self):
        """Test boxInfo method."""
        if len(self.image_info.boxes) > 0:
            # Test with first box
            xmin, ymin, xmax, ymax, confidence, class_name = self.image_info.boxInfo(0)
            
            self.assertIsInstance(xmin, float)
            self.assertIsInstance(ymin, float)
            self.assertIsInstance(xmax, float)
            self.assertIsInstance(ymax, float)
            self.assertIsInstance(confidence, float)
            self.assertIsInstance(class_name, str)
            
            # Check that coordinates are valid
            self.assertLess(xmin, xmax)
            self.assertLess(ymin, ymax)
            self.assertGreaterEqual(confidence, 0.0)
            self.assertLessEqual(confidence, 1.0)
        else:
            self.skipTest("No boxes detected in image")
    
    def test_boxInfo_index_error(self):
        """Test boxInfo with invalid index."""
        invalid_index = len(self.image_info.boxes) + 100
        with self.assertRaises(IndexError):
            self.image_info.boxInfo(invalid_index)
    
    def test_dataFrame(self):
        """Test dataFrame method."""
        df = self.image_info.dataFrame()
        
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        
        # Check columns
        expected_columns = ['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class_name']
        for col in expected_columns:
            self.assertIn(col, df.columns)
        
        # Check that DataFrame has correct number of rows
        self.assertEqual(len(df), len(self.image_info.boxes))
    
    def test_suitcaseHandbagPerson(self):
        """Test suitcaseHandbagPerson method."""
        threshold = 0.5
        result = self.image_info.suitcaseHandbagPerson(threshold)
        
        self.assertIsInstance(result, dict)
        
        # Check that values are either None or tuple
        for key, value in result.items():
            self.assertIsInstance(key, int)
            if value is not None:
                self.assertIsInstance(value, tuple)
                self.assertEqual(len(value), 2)
                person_idx, distance = value
                self.assertIsInstance(person_idx, int)
                self.assertIsInstance(distance, (int, float))
                self.assertGreaterEqual(distance, 0.0)
                self.assertLessEqual(distance, threshold)
    
    def test_suitcaseHandbagPerson_threshold(self):
        """Test suitcaseHandbagPerson with different thresholds."""
        # Test with very small threshold
        result_small = self.image_info.suitcaseHandbagPerson(0.01)
        
        # Test with large threshold
        result_large = self.image_info.suitcaseHandbagPerson(1.0)
        
        self.assertIsInstance(result_small, dict)
        self.assertIsInstance(result_large, dict)
        
        # With larger threshold, we should have same or more matches
        # (or None values if no luggage detected)
        luggage_count = len(result_small)
        self.assertEqual(luggage_count, len(result_large))


if __name__ == '__main__':
    unittest.main()

