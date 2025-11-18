# HW#34 Definition

## Write code creating

- 30 circle images with different random x, y, radius
- 30 square images with different random x, y, width
- 30 labels matching the 30 above circle images
- 30 labels matching the 30 above square images
- 3 circles for validation (val)
- 3 squares for validation
- 3 labels matching the 3 above circle images for validation
- 3 labels matching the 3 above square images for validation

## Update item "names" in data.yaml file

Create configuration file for YOLO training with proper class names.

## Train and create model (best.pt)

Train YOLOv8 model and generate the best performing model.

## Test created model on some image downloaded from Internet containing circles and squares

- Color doesn't matter
- Find out image containing combination of circles and squares

## Note

Try to get rid of copy/pastes in the code (DRY principle).

---

## Solution Structure

```
python-ai-assignment/
├── generate_dataset.py      # Dataset generator (both simple and advanced)
├── train_yolo.py            # Training script
├── test_model.py            # Testing script (local)
├── test_colab.py            # Testing script (Google Colab)
├── create_yaml.py           # YAML generator
├── data.yaml                # YOLO configuration
├── image_info.py            # ImageInfo class (HW#33)
├── test_image_info.py       # Tests for ImageInfo
├── datasets/
│   ├── data.yaml
│   ├── train/
│   │   ├── images/         # 60 training images
│   │   └── labels/         # 60 training labels
│   └── val/
│       ├── images/         # 6 validation images
│       └── labels/         # 6 validation labels
└── runs/                    # Training results
    └── detect/
        └── circle_square_detector/
            └── weights/
                └── best.pt  # Trained model
```

## Usage

### 1. Generate Dataset
```bash
python3 generate_dataset.py
```

### 2. Train Model
```bash
python3 train_yolo.py
```

### 3. Test Model
```bash
python3 test_model.py
```

## Requirements

```bash
pip install ultralytics pandas numpy Pillow
```

## Repository

- **Main branch:** HW#33 - ImageInfo class
- **hw34 branch:** HW#34 - YOLO training dataset
