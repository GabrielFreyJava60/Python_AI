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
        
        # Get the first result (single image)
        self.result = self.results[0]
        
        # Get image dimensions
        self.image_width = self.result.orig_shape[1]
        self.image_height = self.result.orig_shape[0]
        
        # Store boxes for easy access
        self.boxes = self.result.boxes
    
    def boxesClass(self, class_name: str) -> list:
        """
        Get box indices matching the given class name.
        
        Args:
            class_name: Name of the class to filter
            
        Returns:
            List of box indices matching the class
        """
        indices = []
        for i, box in enumerate(self.boxes):
            cls_id = int(box.cls[0])
            cls_name = self.model.names[cls_id]
            if cls_name == class_name:
                indices.append(i)
        return indices
    
    def boxInfo(self, box_index: int) -> tuple:
        """
        Get information about a specific box.
        
        Args:
            box_index: Index of the box
            
        Returns:
            Tuple (xmin, ymin, xmax, ymax, confidence, class_name)
        """
        if box_index >= len(self.boxes):
            raise IndexError(f"Box index {box_index} out of range")
        
        box = self.boxes[box_index]
        
        # Get bounding box coordinates
        xyxy = box.xyxy[0].cpu().numpy()
        xmin, ymin, xmax, ymax = float(xyxy[0]), float(xyxy[1]), float(xyxy[2]), float(xyxy[3])
        
        # Get confidence
        confidence = float(box.conf[0].cpu().numpy())
        
        # Get class name
        cls_id = int(box.cls[0])
        class_name = self.model.names[cls_id]
        
        return (xmin, ymin, xmax, ymax, confidence, class_name)
    
    def dataFrame(self) -> pd.DataFrame:
        """
        Create a pandas DataFrame with all detection information.
        
        Returns:
            DataFrame with columns: xmin, ymin, xmax, ymax, confidence, class_name
        """
        data = []
        for i in range(len(self.boxes)):
            xmin, ymin, xmax, ymax, confidence, class_name = self.boxInfo(i)
            data.append({
                'xmin': xmin,
                'ymin': ymin,
                'xmax': xmax,
                'ymax': ymax,
                'confidence': confidence,
                'class_name': class_name
            })
        
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
        # Get indices of suitcases, handbags, and persons
        suitcase_indices = self.boxesClass("suitcase")
        handbag_indices = self.boxesClass("handbag")
        person_indices = self.boxesClass("person")
        
        # Combine suitcase and handbag indices
        luggage_indices = suitcase_indices + handbag_indices
        
        result = {}
        
        for luggage_idx in luggage_indices:
            luggage_box = self.boxes[luggage_idx]
            luggage_xywhn = luggage_box.xywhn[0].cpu().numpy()
            luggage_x_center = luggage_xywhn[0]
            luggage_y_center = luggage_xywhn[1]
            
            min_distance = float('inf')
            matched_person_idx = None
            
            # Find the nearest person
            for person_idx in person_indices:
                person_box = self.boxes[person_idx]
                person_xywhn = person_box.xywhn[0].cpu().numpy()
                person_x_center = person_xywhn[0]
                person_y_center = person_xywhn[1]
                
                # Calculate normalized distance between centers
                dx = luggage_x_center - person_x_center
                dy = luggage_y_center - person_y_center
                distance = np.sqrt(dx**2 + dy**2)
                
                if distance < min_distance:
                    min_distance = distance
                    matched_person_idx = person_idx
            
            # Check if distance is within threshold
            if matched_person_idx is not None and min_distance <= threshold:
                result[luggage_idx] = (matched_person_idx, min_distance)
            else:
                result[luggage_idx] = None
        
        return result

