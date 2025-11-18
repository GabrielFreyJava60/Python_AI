import requests
from PIL import Image
from io import BytesIO
from ultralytics import YOLO
from image_info import ImageInfo


def test_model_with_url(model_path, image_url):
    print("📥 Downloading image...")
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save("temp_test.jpg")
    
    print("🔧 Loading model...")
    model = YOLO(model_path)
    
    print("🔮 Running prediction...")
    results = model.predict("temp_test.jpg", save=True, conf=0.5)
    
    print("\n✅ Complete!")
    
    result_img = results[0].plot()
    result_pil = Image.fromarray(result_img)
    
    print("\n📊 Detections via YOLO:")
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = model.names[class_id]
        print(f"  • {class_name}: {confidence:.2%}")
    
    print("\n🔍 Validation via ImageInfo (HW#33):")
    img_info = ImageInfo("temp_test.jpg")
    df = img_info.dataFrame()
    print(f"  Total objects detected: {len(df)}")
    
    circles = img_info.boxesClass("circle")
    squares = img_info.boxesClass("square")
    print(f"  🔵 Circles: {len(circles)}")
    print(f"  🟦 Squares: {len(squares)}")
    
    return result_pil


if __name__ == "__main__":
    model_path = "runs/detect/circle_square_detector/weights/best.pt"
    image_url = "https://picsum.photos/640/640"
    
    result_image = test_model_with_url(model_path, image_url)
    result_image.show()

