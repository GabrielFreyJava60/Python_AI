import os
import random
from pathlib import Path
from typing import Tuple, List
from PIL import Image, ImageDraw


class YOLODatasetGenerator:
    
    def __init__(self, base_dir: str = "datasets", img_size: Tuple[int, int] = (640, 640)):
        self.base_dir = Path(base_dir)
        self.img_size = img_size
        self.classes = {0: "circle", 1: "square"}
        
    def setup_directories(self):
        for split in ["train", "val"]:
            (self.base_dir / split / "images").mkdir(parents=True, exist_ok=True)
            (self.base_dir / split / "labels").mkdir(parents=True, exist_ok=True)
    
    def _generate_random_params(self) -> dict:
        min_size = min(self.img_size) // 8
        max_size = min(self.img_size) // 3
        size = random.randint(min_size, max_size)
        
        x = random.randint(size, self.img_size[0] - size)
        y = random.randint(size, self.img_size[1] - size)
        
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        
        return {"x": x, "y": y, "size": size, "color": color}
    
    def _draw_shape(self, draw: ImageDraw, shape_type: str, params: dict):
        x, y, size = params["x"], params["y"], params["size"]
        color = params["color"]
        
        if shape_type == "circle":
            bbox = [x - size, y - size, x + size, y + size]
            draw.ellipse(bbox, fill=color, outline=(0, 0, 0), width=2)
        elif shape_type == "square":
            bbox = [x - size, y - size, x + size, y + size]
            draw.rectangle(bbox, fill=color, outline=(0, 0, 0), width=2)
    
    def _calculate_yolo_bbox(self, params: dict) -> Tuple[float, float, float, float]:
        x, y, size = params["x"], params["y"], params["size"]
        
        x_center = x / self.img_size[0]
        y_center = y / self.img_size[1]
        width = (size * 2) / self.img_size[0]
        height = (size * 2) / self.img_size[1]
        
        return x_center, y_center, width, height
    
    def generate_image(self, class_id: int, split: str, index: int):
        shape_type = self.classes[class_id]
        
        img = Image.new("RGB", self.img_size, color="white")
        draw = ImageDraw.Draw(img)
        
        params = self._generate_random_params()
        self._draw_shape(draw, shape_type, params)
        
        img_path = self.base_dir / split / "images" / f"{shape_type}_{index}.jpg"
        img.save(img_path, quality=95)
        
        x_center, y_center, width, height = self._calculate_yolo_bbox(params)
        label_path = self.base_dir / split / "labels" / f"{shape_type}_{index}.txt"
        with open(label_path, "w") as f:
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        return img_path, label_path
    
    def generate_dataset(self, train_per_class: int = 30, val_per_class: int = 3):
        self.setup_directories()
        
        total_images = 0
        
        for split, count in [("train", train_per_class), ("val", val_per_class)]:
            print(f"\n📂 Generating {split} set...")
            
            for class_id, class_name in self.classes.items():
                for i in range(count):
                    img_path, label_path = self.generate_image(class_id, split, i)
                    total_images += 1
                    
                    if (i + 1) % 10 == 0 or i == count - 1:
                        print(f"  ✓ {class_name}: {i + 1}/{count} images")
        
        print(f"\n✅ Dataset generation complete!")
        print(f"📊 Total images: {total_images}")
        print(f"📁 Location: {self.base_dir.absolute()}")
        
        self._generate_yaml()
    
    def _generate_yaml(self):
        yaml_content = f"""path: {self.base_dir.absolute()}
train: train/images
val: val/images

nc: {len(self.classes)}
names: {list(self.classes.values())}
"""
        yaml_path = self.base_dir / "data.yaml"
        with open(yaml_path, "w") as f:
            f.write(yaml_content)
        
        print(f"📄 Created: {yaml_path}")


def main():
    print("🎨 YOLO Synthetic Dataset Generator")
    print("=" * 50)
    
    generator = YOLODatasetGenerator(base_dir="datasets", img_size=(640, 640))
    generator.generate_dataset(train_per_class=30, val_per_class=3)
    
    print("\n" + "=" * 50)
    print("🚀 Ready to train YOLO!")


if __name__ == "__main__":
    main()

