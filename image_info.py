import pandas as pd
import numpy as np
from ultralytics import YOLO
from pathlib import Path


class ImageInfo:
    
    def __init__(self, image_path: str):
        self.image_path = Path(image_path)
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        self.model = YOLO("yolov8m-seg.pt")
        self.results = self.model(str(self.image_path))
        self.boxes = self.results[0].boxes
    
    def boxesClass(self, class_name: str) -> list:
        return [i for i, box in enumerate(self.boxes) 
                if self.model.names[int(box.cls[0])] == class_name]
    
    def boxInfo(self, box_index: int) -> tuple:
        if not 0 <= box_index < len(self.boxes):
            raise IndexError(f"Box index {box_index} out of range")
        
        box = self.boxes[box_index]
        xyxy = box.xyxy[0].cpu().numpy()
        
        return (
            float(xyxy[0]),
            float(xyxy[1]),
            float(xyxy[2]),
            float(xyxy[3]),
            float(box.conf[0]),
            self.model.names[int(box.cls[0])]
        )
    
    def dataFrame(self) -> pd.DataFrame:
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
        luggage_indices = self.boxesClass("suitcase") + self.boxesClass("handbag")
        person_indices = self.boxesClass("person")
        
        result = {}
        
        for luggage_idx in luggage_indices:
            luggage_center = self.boxes[luggage_idx].xywhn[0].cpu().numpy()[:2]
            
            min_distance = float('inf')
            matched_person_idx = None
            
            for person_idx in person_indices:
                person_center = self.boxes[person_idx].xywhn[0].cpu().numpy()[:2]
                distance = float(np.linalg.norm(luggage_center - person_center))
                
                if distance < min_distance:
                    min_distance = distance
                    matched_person_idx = person_idx
            
            result[luggage_idx] = (
                (matched_person_idx, min_distance) 
                if matched_person_idx is not None and min_distance <= threshold 
                else None
            )
        
        return result

