import os

def create_data_yaml(path="datasets"):
    
    os.makedirs(path, exist_ok=True)
    
    yaml_content = f"""path: {path}
train: train/images
val: val/images

nc: 2
names: ['circle', 'square']
"""
    
    output_path = f"{path}/data.yaml"
    
    with open(output_path, "w") as f:
        f.write(yaml_content)
    
    print(f"✅ Created: {output_path}")
    print("\nFile content:")
    print("-" * 40)
    print(yaml_content)
    print("-" * 40)


if __name__ == "__main__":
    create_data_yaml("datasets")

