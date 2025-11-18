import random
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageDraw


class ShapeDrawer:
    
    @staticmethod
    def get_random_params(img_size: Tuple[int, int]) -> dict:
        min_size = min(img_size) // 8
        max_size = min(img_size) // 3
        size = random.randint(min_size, max_size)
        
        x = random.randint(size, img_size[0] - size)
        y = random.randint(size, img_size[1] - size)
        
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        
        return {"x": x, "y": y, "size": size, "color": color}
    
    @staticmethod
    def draw_shape(draw: ImageDraw, shape_type: str, params: dict):
        x, y, size = params["x"], params["y"], params["size"]
        color = params["color"]
        bbox = [x - size, y - size, x + size, y + size]
        
        if shape_type == "circle":
            draw.ellipse(bbox, fill=color, outline=(0, 0, 0), width=2)
        elif shape_type == "square":
            draw.rectangle(bbox, fill=color, outline=(0, 0, 0), width=2)


class YOLODatasetGenerator:
    
    SHAPES = {0: "circle", 1: "square"}
    
    def __init__(self, base_dir: str = "datasets", img_size: Tuple[int, int] = (640, 640)):
        self.base_dir = Path(base_dir)
        self.img_size = img_size
        self.drawer = ShapeDrawer()
        
    def setup_directories(self):
        for split in ["train", "val"]:
            (self.base_dir / split / "images").mkdir(parents=True, exist_ok=True)
            (self.base_dir / split / "labels").mkdir(parents=True, exist_ok=True)
    
    def calculate_yolo_bbox(self, params: dict) -> Tuple[float, float, float, float]:
        x_center = params["x"] / self.img_size[0]
        y_center = params["y"] / self.img_size[1]
        width = (params["size"] * 2) / self.img_size[0]
        height = (params["size"] * 2) / self.img_size[1]
        
        return x_center, y_center, width, height
    
    def generate_image(self, class_id: int, split: str, index: int):
        shape_type = self.SHAPES[class_id]
        
        img = Image.new("RGB", self.img_size, color="white")
        draw = ImageDraw.Draw(img)
        
        params = self.drawer.get_random_params(self.img_size)
        self.drawer.draw_shape(draw, shape_type, params)
        
        img_path = self.base_dir / split / "images" / f"{shape_type}_{index}.jpg"
        img.save(img_path, quality=95)
        
        x_center, y_center, width, height = self.calculate_yolo_bbox(params)
        label_path = self.base_dir / split / "labels" / f"{shape_type}_{index}.txt"
        with open(label_path, "w") as f:
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        return img_path, label_path
    
    def generate_dataset(self, train_per_class: int = 30, val_per_class: int = 3):
        self.setup_directories()
        
        total_images = 0
        
        for split, count in [("train", train_per_class), ("val", val_per_class)]:
            print(f"\n📂 Generating {split} set...")
            
            for class_id, class_name in self.SHAPES.items():
                for i in range(count):
                    self.generate_image(class_id, split, i)
                    total_images += 1
                    
                    if (i + 1) % 10 == 0 or i == count - 1:
                        print(f"  ✓ {class_name}: {i + 1}/{count} images")
        
        print(f"\n✅ Dataset generation complete!")
        print(f"📊 Total images: {total_images}")
        
        self.generate_yaml()
    
    def generate_yaml(self):
        yaml_content = f"""path: {self.base_dir}
train: train/images
val: val/images

nc: {len(self.SHAPES)}
names: {list(self.SHAPES.values())}
"""
        yaml_path = self.base_dir / "data.yaml"
        with open(yaml_path, "w") as f:
            f.write(yaml_content)
        
        print(f"📄 Created: {yaml_path}")


def main():
    print("=" * 60)
    print("🎯 YOLO DATASET GENERATOR")
    print("=" * 60)
    
    generator = YOLODatasetGenerator(base_dir="datasets", img_size=(640, 640))
    generator.generate_dataset(train_per_class=30, val_per_class=3)
    
    print("\n" + "=" * 60)
    print("🚀 Dataset is ready for YOLO training!")
    print("=" * 60)


if __name__ == "__main__":
    main()
