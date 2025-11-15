"""
ImageInfo class for YOLO object detection and analysis.
"""
import pandas as pd
import numpy as np
from ultralytics import YOLO
from pathlib import Path


class ImageInfo:
    """
    Class for analyzing images using YOLO segmentation model.
    """
    
    def __init__(self, image_path: str):
        """
        Initialize ImageInfo with image path.
        
        Args:
            image_path: Path to the image file
            
        Note:
            Uses model "yolov8m-seg.pt" for segmentation
        """
        self.image_path = Path(image_path)
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Load YOLO segmentation model
        self.model = YOLO("yolov8m-seg.pt")
        
        # Run inference
        self.results = self.model(str(self.image_path))
        
        # Get the first result (single image) and store boxes
        self.boxes = self.results[0].boxes
    
    def boxesClass(self, class_name: str) -> list:
        """
        Get box indices matching the given class name.
        
        Args:
            class_name: Name of the class to filter
            
        Returns:
            List of box indices matching the class
        """
        return [i for i, box in enumerate(self.boxes) 
                if self.model.names[int(box.cls[0])] == class_name]
    
    def boxInfo(self, box_index: int) -> tuple:
        """
        Get information about a specific box.
        
        Args:
            box_index: Index of the box
            
        Returns:
            Tuple (xmin, ymin, xmax, ymax, confidence, class_name)
        """
        if not 0 <= box_index < len(self.boxes):
            raise IndexError(f"Box index {box_index} out of range")
        
        box = self.boxes[box_index]
        xyxy = box.xyxy[0].cpu().numpy()
        
        return (
            float(xyxy[0]),  # xmin
            float(xyxy[1]),  # ymin
            float(xyxy[2]),  # xmax
            float(xyxy[3]),  # ymax
            float(box.conf[0]),  # confidence
            self.model.names[int(box.cls[0])]  # class_name
        )
    
    def dataFrame(self) -> pd.DataFrame:
        """
        Create a pandas DataFrame with all detection information.
        
        Returns:
            DataFrame with columns: xmin, ymin, xmax, ymax, confidence, class_name
        """
        data = [
            {
                'xmin': xmin,
                'ymin': ymin,
                'xmax': xmax,
                'ymax': ymax,
                'confidence': confidence,
                'class_name': class_name
            }
            for i in range(len(self.boxes))
            for xmin, ymin, xmax, ymax, confidence, class_name in [self.boxInfo(i)]
        ]
        return pd.DataFrame(data)
    
    def suitcaseHandbagPerson(self, threshold: float) -> dict:
        """
        Match suitcases/handbags with nearest persons.
        
        Args:
            threshold: Normalized distance threshold [0-1]
            
        Returns:
            Dictionary where:
            - key: index of suitcase/handbag box
            - value: tuple (person_box_index, normalized_distance) or None if distance > threshold
        """
        luggage_indices = self.boxesClass("suitcase") + self.boxesClass("handbag")
        person_indices = self.boxesClass("person")
        
        result = {}
        
        for luggage_idx in luggage_indices:
            # Get luggage center coordinates (normalized)
            luggage_center = self.boxes[luggage_idx].xywhn[0].cpu().numpy()[:2]
            
            min_distance = float('inf')
            matched_person_idx = None
            
            # Find the nearest person
            for person_idx in person_indices:
                person_center = self.boxes[person_idx].xywhn[0].cpu().numpy()[:2]
                distance = float(np.linalg.norm(luggage_center - person_center))
                
                if distance < min_distance:
                    min_distance = distance
                    matched_person_idx = person_idx
            
            # Store result if within threshold
            result[luggage_idx] = (
                (matched_person_idx, min_distance) 
                if matched_person_idx is not None and min_distance <= threshold 
                else None
            )
        
        return result

