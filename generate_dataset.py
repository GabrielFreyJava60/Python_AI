import os
import random
from pathlib import Path
from typing import Tuple
from PIL import Image, ImageDraw


IMAGE_WIDTH = 640
IMAGE_HEIGHT = 640
TRAIN_CIRCLES = 30
TRAIN_SQUARES = 30
VAL_CIRCLES = 3
VAL_SQUARES = 3
CLASS_CIRCLE = 0
CLASS_SQUARE = 1


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
        
        self._generate_yaml()
    
    def _generate_yaml(self):
        yaml_content = f"""path: {self.base_dir}
train: train/images
val: val/images

nc: {len(self.classes)}
names: {list(self.classes.values())}
"""
        yaml_path = self.base_dir / "data.yaml"
        with open(yaml_path, "w") as f:
            f.write(yaml_content)
        
        print(f"📄 Created: {yaml_path}")


def create_folders():
    folders = [
        "datasets/train/images",
        "datasets/train/labels",
        "datasets/val/images",
        "datasets/val/labels"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


def get_random_color():
    return (
        random.randint(50, 255),
        random.randint(50, 255),
        random.randint(50, 255)
    )


def get_random_size():
    return random.randint(IMAGE_WIDTH // 8, IMAGE_WIDTH // 3)


def get_random_position(size):
    center_x = random.randint(size, IMAGE_WIDTH - size)
    center_y = random.randint(size, IMAGE_HEIGHT - size)
    return (center_x, center_y)


def draw_circle(draw, center_x, center_y, size, color):
    bbox = [center_x - size, center_y - size, center_x + size, center_y + size]
    draw.ellipse(bbox, fill=color, outline=(0, 0, 0), width=2)


def draw_square(draw, center_x, center_y, size, color):
    bbox = [center_x - size, center_y - size, center_x + size, center_y + size]
    draw.rectangle(bbox, fill=color, outline=(0, 0, 0), width=2)


def calculate_yolo_label(center_x, center_y, size):
    normalized_x_center = center_x / IMAGE_WIDTH
    normalized_y_center = center_y / IMAGE_HEIGHT
    normalized_width = (size * 2) / IMAGE_WIDTH
    normalized_height = (size * 2) / IMAGE_HEIGHT
    
    return (normalized_x_center, normalized_y_center, normalized_width, normalized_height)


def create_image_and_label(shape_type, folder, index):
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color="white")
    draw = ImageDraw.Draw(image)
    
    color = get_random_color()
    size = get_random_size()
    center_x, center_y = get_random_position(size)
    
    if shape_type == "circle":
        draw_circle(draw, center_x, center_y, size, color)
        class_id = CLASS_CIRCLE
    else:
        draw_square(draw, center_x, center_y, size, color)
        class_id = CLASS_SQUARE
    
    image_path = f"datasets/{folder}/images/{shape_type}_{index}.jpg"
    image.save(image_path, quality=95)
    
    x_center, y_center, width, height = calculate_yolo_label(center_x, center_y, size)
    
    label_path = f"datasets/{folder}/labels/{shape_type}_{index}.txt"
    with open(label_path, "w") as file:
        file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")


def generate_dataset_simple():
    print("\n🎨 Starting dataset generation...\n")
    
    create_folders()
    
    print("📚 Generating TRAINING set...")
    
    for i in range(TRAIN_CIRCLES):
        create_image_and_label("circle", "train", i)
    print(f"  ✓ Created {TRAIN_CIRCLES} circle images")
    
    for i in range(TRAIN_SQUARES):
        create_image_and_label("square", "train", i)
    print(f"  ✓ Created {TRAIN_SQUARES} square images")
    
    print("\n🔍 Generating VALIDATION set...")
    
    for i in range(VAL_CIRCLES):
        create_image_and_label("circle", "val", i)
    print(f"  ✓ Created {VAL_CIRCLES} circle images")
    
    for i in range(VAL_SQUARES):
        create_image_and_label("square", "val", i)
    print(f"  ✓ Created {VAL_SQUARES} square images")
    
    yaml_content = """path: datasets
train: train/images
val: val/images

nc: 2
names: ['circle', 'square']
"""
    
    with open("datasets/data.yaml", "w") as file:
        file.write(yaml_content)
    
    print(f"\n✅ Complete!")
    print(f"📊 Training: {TRAIN_CIRCLES + TRAIN_SQUARES} images")
    print(f"📊 Validation: {VAL_CIRCLES + VAL_SQUARES} images")


def main():
    print("=" * 60)
    print("🎯 YOLO DATASET GENERATOR")
    print("=" * 60)
    print("\nChoose version:")
    print("  1. Advanced (Class-based)")
    print("  2. Simple (Function-based)")
    
    choice = input("\nEnter choice (1/2) or press Enter for Simple: ").strip()
    
    if choice == "1":
        print("\n🔧 Using Advanced version...")
        generator = YOLODatasetGenerator(base_dir="datasets", img_size=(640, 640))
        generator.generate_dataset(train_per_class=30, val_per_class=3)
    else:
        print("\n🔧 Using Simple version...")
        generate_dataset_simple()
    
    print("\n" + "=" * 60)
    print("🚀 Dataset is ready for YOLO training!")
    print("=" * 60)


if __name__ == "__main__":
    main()
