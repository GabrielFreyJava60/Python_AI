import requests
from PIL import Image
from io import BytesIO
from IPython.display import display
from ultralytics import YOLO


model_path = "runs/detect/train/weights/best.pt"
image_url = "https://picsum.photos/640/640"

print("📥 Downloading image...")
response = requests.get(image_url)
original_image = Image.open(BytesIO(response.content))

print("📷 Original Image:")
display(original_image)

print("\n🔧 Loading model...")
model = YOLO(model_path)

print("\n🔮 Running prediction...")
results = model.predict(original_image, save=True, conf=0.25)

print("\n✅ Result:")
result_img_array = results[0].plot()
result_image = Image.fromarray(result_img_array)
display(result_image)

print("\n📊 Detections:")
if len(results[0].boxes) == 0:
    print("  No objects detected")
else:
    for i, box in enumerate(results[0].boxes):
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = model.names[class_id]
        print(f"  {i+1}. {class_name}: {confidence:.1%}")

