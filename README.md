# HW#33 - ImageInfo Class

## Описание

Реализация класса `ImageInfo` для анализа изображений с использованием модели YOLO segmentation.

## Требования

- Python 3.8+
- ultralytics
- pandas
- Pillow
- numpy

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```python
from image_info import ImageInfo

# Инициализация с путем к изображению
image_info = ImageInfo("path/to/image.jpg")

# Получить индексы боксов определенного класса
person_indices = image_info.boxesClass("person")

# Получить информацию о конкретном боксе
xmin, ymin, xmax, ymax, confidence, class_name = image_info.boxInfo(0)

# Получить DataFrame со всеми детекциями
df = image_info.dataFrame()

# Найти соответствия между сумками/чемоданами и людьми
matches = image_info.suitcaseHandbagPerson(threshold=0.5)
```

## Методы класса

### `__init__(image_path: str)`
Конструктор, принимающий путь к изображению. Использует модель "yolov8m-seg.pt".

### `boxesClass(class_name: str) -> list`
Возвращает индексы боксов, соответствующих заданному классу.

### `boxInfo(box_index: int) -> tuple`
Возвращает кортеж (xmin, ymin, xmax, ymax, confidence, class_name) для указанного бокса.

### `dataFrame() -> pd.DataFrame`
Возвращает pandas DataFrame со всеми детекциями.

### `suitcaseHandbagPerson(threshold: float) -> dict`
Возвращает словарь, где ключ - индекс бокса сумки/чемодана, значение - кортеж (индекс бокса человека, нормализованное расстояние) или None, если расстояние превышает порог.

## Тестирование

```bash
python test_image_info.py
```

## Примечания

- Модель "yolov8m-seg.pt" будет автоматически загружена при первом использовании
- Для тестирования требуется изображение с объектами (например, street.jpg)

