import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from converter import columnsMapper, convertX


df = pd.read_csv('car_sales_data.csv')

print("=" * 60)
print("HW#30: Creating predictions model and working with pandas")
print("=" * 60)

print("\n1. Creating prediction model")
print("-" * 60)

X_columns = ['Gender', 'Color']
y_column = 'Model'

X_df = df[X_columns].copy()
y_series = df[y_column].copy()

mapper_X = columnsMapper(X_df, X_columns)
X_encoded = convertX(X_df, mapper_X)

mapper_y = columnsMapper(pd.DataFrame({y_column: y_series}), [y_column])
y_encoded = convertX(pd.DataFrame({y_column: y_series}), mapper_y)[y_column]

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y_encoded, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

model_filename = 'car_model_predictor.joblib'
joblib.dump(model, model_filename)
print(f"Model saved to: {model_filename}")

mapper_filename = 'car_model_mappers.joblib'
joblib.dump({'X': mapper_X, 'y': mapper_y}, mapper_filename)
print(f"Mappers saved to: {mapper_filename}")

print("\n2. Working with pandas")
print("-" * 60)

hyundai_df = df[df['Company'] == 'Hyundai'].copy()
print(f"\nDataFrame containing only Hyundai data:")
print(f"Number of rows: {len(hyundai_df)}")
print(f"\nFirst 5 rows:")
print(hyundai_df.head())

toyota_expensive_df = df[(df['Company'] == 'Toyota') & (df['Price'] > 40000)].copy()
print(f"\nDataFrame containing only Toyota with price > 40000:")
print(f"Number of rows: {len(toyota_expensive_df)}")
print(f"\nFirst 5 rows:")
print(toyota_expensive_df.head())

model_counts = df['Model'].value_counts()
top_3_models = model_counts.head(3)
print(f"\n3 most popular car models:")
for model_name, count in top_3_models.items():
    print(f"  {model_name}: {count} occurrences")

print("\n" + "=" * 60)
print("All tasks completed!")
print("=" * 60)

