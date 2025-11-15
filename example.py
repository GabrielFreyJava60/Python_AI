"""
Example usage of ImageInfo class.
"""
from image_info import ImageInfo

# Replace with your image path
IMAGE_PATH = "street.jpg"  # or any other image

def main():
    print("=" * 60)
    print("ImageInfo Class - Example Usage")
    print("=" * 60)
    
    # Initialize
    print(f"\n1. Initializing with image: {IMAGE_PATH}")
    image_info = ImageInfo(IMAGE_PATH)
    print(f"   ✓ Model loaded: yolov8m-seg.pt")
    print(f"   ✓ Detected {len(image_info.boxes)} objects")
    
    # Get all detected classes
    print("\n2. Detected classes:")
    classes = set()
    for i in range(len(image_info.boxes)):
        _, _, _, _, _, class_name = image_info.boxInfo(i)
        classes.add(class_name)
    print(f"   {', '.join(sorted(classes))}")
    
    # Test boxesClass
    print("\n3. Testing boxesClass method:")
    person_indices = image_info.boxesClass("person")
    print(f"   Found {len(person_indices)} person(s) at indices: {person_indices}")
    
    # Test boxInfo
    if len(image_info.boxes) > 0:
        print("\n4. Testing boxInfo method (first detection):")
        xmin, ymin, xmax, ymax, conf, cls = image_info.boxInfo(0)
        print(f"   Class: {cls}")
        print(f"   Confidence: {conf:.2f}")
        print(f"   BBox: ({xmin:.1f}, {ymin:.1f}) -> ({xmax:.1f}, {ymax:.1f})")
    
    # Test dataFrame
    print("\n5. Testing dataFrame method:")
    df = image_info.dataFrame()
    print(f"   DataFrame shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    if len(df) > 0:
        print("\n   First 3 rows:")
        print(df.head(3).to_string(index=False))
    
    # Test suitcaseHandbagPerson
    print("\n6. Testing suitcaseHandbagPerson method:")
    matches = image_info.suitcaseHandbagPerson(threshold=0.5)
    if matches:
        print(f"   Found {len(matches)} luggage item(s)")
        for luggage_idx, match in matches.items():
            if match:
                person_idx, distance = match
                print(f"   - Luggage[{luggage_idx}] -> Person[{person_idx}] (distance: {distance:.3f})")
            else:
                print(f"   - Luggage[{luggage_idx}] -> No nearby person (distance > 0.5)")
    else:
        print("   No suitcases or handbags detected")
    
    print("\n" + "=" * 60)
    print("✓ All methods tested successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()

