from ultralytics import YOLO

def train_model():
    print("🔧 Loading model...")
    model = YOLO('yolov8n.pt')
    
    print("\n🚀 Starting training...\n")
    results = model.train(
        data='datasets/data.yaml',
        epochs=20,
        imgsz=640,
        batch=16,
        name='circle_square_detector'
    )
    
    print("\n✅ Complete!")
    print("📦 Best model: runs/detect/circle_square_detector/weights/best.pt")


if __name__ == "__main__":
    train_model()

