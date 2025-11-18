import os
import random
from PIL import Image, ImageDraw


IMAGE_WIDTH = 640
IMAGE_HEIGHT = 640
TRAIN_CIRCLES = 30
TRAIN_SQUARES = 30
VAL_CIRCLES = 3
VAL_SQUARES = 3

CLASS_CIRCLE = 0
CLASS_SQUARE = 1


def create_folders():
    print("📁 Creating folders...")
    
    folders = [
        "datasets/train/images",
        "datasets/train/labels",
        "datasets/val/images",
        "datasets/val/labels"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"  ✓ Created: {folder}")


def get_random_color():
    red = random.randint(50, 255)
    green = random.randint(50, 255)
    blue = random.randint(50, 255)
    
    return (red, green, blue)


def get_random_size():
    min_size = IMAGE_WIDTH // 8
    max_size = IMAGE_WIDTH // 3
    size = random.randint(min_size, max_size)
    
    return size


def get_random_position(size):
    min_x = size
    max_x = IMAGE_WIDTH - size
    min_y = size
    max_y = IMAGE_HEIGHT - size
    
    center_x = random.randint(min_x, max_x)
    center_y = random.randint(min_y, max_y)
    
    return (center_x, center_y)


def draw_circle(draw, center_x, center_y, size, color):
    left = center_x - size
    top = center_y - size
    right = center_x + size
    bottom = center_y + size
    
    draw.ellipse([left, top, right, bottom], 
                 fill=color, 
                 outline=(0, 0, 0), 
                 width=2)


def draw_square(draw, center_x, center_y, size, color):
    left = center_x - size
    top = center_y - size
    right = center_x + size
    bottom = center_y + size
    
    draw.rectangle([left, top, right, bottom], 
                   fill=color, 
                   outline=(0, 0, 0), 
                   width=2)


def calculate_yolo_label(center_x, center_y, size):
    normalized_x_center = center_x / IMAGE_WIDTH
    normalized_y_center = center_y / IMAGE_HEIGHT
    
    bbox_width = size * 2
    bbox_height = size * 2
    
    normalized_width = bbox_width / IMAGE_WIDTH
    normalized_height = bbox_height / IMAGE_HEIGHT
    
    return (normalized_x_center, normalized_y_center, 
            normalized_width, normalized_height)


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
    
    image_filename = f"{shape_type}_{index}.jpg"
    image_path = f"datasets/{folder}/images/{image_filename}"
    image.save(image_path, quality=95)
    
    x_center, y_center, width, height = calculate_yolo_label(center_x, center_y, size)
    
    label_filename = f"{shape_type}_{index}.txt"
    label_path = f"datasets/{folder}/labels/{label_filename}"
    
    with open(label_path, "w") as file:
        file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")


def generate_dataset():
    print("\n🎨 Starting dataset generation...\n")
    
    total_images = 0
    
    print("📚 Generating TRAINING set...")
    
    for i in range(TRAIN_CIRCLES):
        create_image_and_label("circle", "train", i)
        total_images += 1
    print(f"  ✓ Created {TRAIN_CIRCLES} circle images")
    
    for i in range(TRAIN_SQUARES):
        create_image_and_label("square", "train", i)
        total_images += 1
    print(f"  ✓ Created {TRAIN_SQUARES} square images")
    
    print("\n🔍 Generating VALIDATION set...")
    
    for i in range(VAL_CIRCLES):
        create_image_and_label("circle", "val", i)
        total_images += 1
    print(f"  ✓ Created {VAL_CIRCLES} circle images")
    
    for i in range(VAL_SQUARES):
        create_image_and_label("square", "val", i)
        total_images += 1
    print(f"  ✓ Created {VAL_SQUARES} square images")
    
    print(f"\n✅ SUCCESS! Generated {total_images} images total")
    print(f"📊 Training: {TRAIN_CIRCLES + TRAIN_SQUARES} images")
    print(f"📊 Validation: {VAL_CIRCLES + VAL_SQUARES} images")


def create_yaml_file():
    print("\n📄 Creating data.yaml configuration file...")
    
    yaml_content = """path: datasets
train: train/images
val: val/images

nc: 2
names: ['circle', 'square']
"""
    
    with open("datasets/data.yaml", "w") as file:
        file.write(yaml_content)
    
    print("  ✓ Created datasets/data.yaml")


def main():
    print("=" * 60)
    print("🎯 YOLO DATASET GENERATOR")
    print("=" * 60)
    
    create_folders()
    generate_dataset()
    create_yaml_file()
    
    print("\n" + "=" * 60)
    print("🚀 Dataset is ready for YOLO training!")
    print("=" * 60)


if __name__ == "__main__":
    main()
