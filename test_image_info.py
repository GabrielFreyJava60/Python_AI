import unittest
import os
import pandas as pd
from pathlib import Path
from image_info import ImageInfo


class TestImageInfo(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
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
        if self.test_image:
            self.image_info = ImageInfo(self.test_image)
    
    def test_initialization(self):
        self.assertIsNotNone(self.image_info)
        self.assertIsNotNone(self.image_info.model)
        self.assertIsNotNone(self.image_info.results)
        self.assertIsNotNone(self.image_info.boxes)
        self.assertGreater(len(self.image_info.boxes), 0)
    
    def test_boxesClass(self):
        person_indices = self.image_info.boxesClass("person")
        self.assertIsInstance(person_indices, list)
        
        airplane_indices = self.image_info.boxesClass("airplane")
        self.assertIsInstance(airplane_indices, list)
    
    def test_boxInfo(self):
        if len(self.image_info.boxes) > 0:
            xmin, ymin, xmax, ymax, confidence, class_name = self.image_info.boxInfo(0)
            
            self.assertIsInstance(xmin, float)
            self.assertIsInstance(ymin, float)
            self.assertIsInstance(xmax, float)
            self.assertIsInstance(ymax, float)
            self.assertIsInstance(confidence, float)
            self.assertIsInstance(class_name, str)
            
            self.assertLess(xmin, xmax)
            self.assertLess(ymin, ymax)
            self.assertGreaterEqual(confidence, 0.0)
            self.assertLessEqual(confidence, 1.0)
        else:
            self.skipTest("No boxes detected in image")
    
    def test_boxInfo_index_error(self):
        invalid_index = len(self.image_info.boxes) + 100
        with self.assertRaises(IndexError):
            self.image_info.boxInfo(invalid_index)
    
    def test_dataFrame(self):
        df = self.image_info.dataFrame()
        
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        
        expected_columns = ['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class_name']
        for col in expected_columns:
            self.assertIn(col, df.columns)
        
        self.assertEqual(len(df), len(self.image_info.boxes))
    
    def test_suitcaseHandbagPerson(self):
        threshold = 0.5
        result = self.image_info.suitcaseHandbagPerson(threshold)
        
        self.assertIsInstance(result, dict)
        
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
        result_small = self.image_info.suitcaseHandbagPerson(0.01)
        result_large = self.image_info.suitcaseHandbagPerson(1.0)
        
        self.assertIsInstance(result_small, dict)
        self.assertIsInstance(result_large, dict)
        
        luggage_count = len(result_small)
        self.assertEqual(luggage_count, len(result_large))


if __name__ == '__main__':
    unittest.main()

