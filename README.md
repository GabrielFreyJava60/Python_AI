# HW #30 Definition

## Creating predictions model

### Create model for predictions with Gender, Color as input (X) and car's model as output (y)

#### Compute accuracy

#### Persist

## Working with "pandas" package (research task)

### Getting Data Frame containing only data about Hyundai

### Getting Data Frame containing only data about Toyota with price greater than 40000

### Define 3 most popular car's models

## Files

- `hw30.py` - main script implementing all tasks
- `car_sales_data.csv` - dataset with car sales information
- `converter.py` - module from HW29 used for encoding categorical data
- `car_model_predictor.joblib` - saved trained model (generated after running hw30.py)
- `car_model_mappers.joblib` - saved encoders for features and target (generated after running hw30.py)

## Usage

```bash
python3 hw30.py
```

The script will:
1. Load car sales data from CSV
2. Create and train a prediction model using Gender and Color as features
3. Compute and display model accuracy
4. Save the trained model and encoders
5. Filter Hyundai data
6. Filter Toyota data with price > 40000
7. Display 3 most popular car models
