import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from converter import columnsMapper, convertX


def create_prediction_model(df: pd.DataFrame, X_columns: list[str], y_column: str):
    print(f"\nCreating prediction model")
    print(f"Features (X): {X_columns}")
    print(f"Target (y): {y_column}")
    
    X_df = df[X_columns].copy()
    y_series = df[y_column].copy()
    
    mapper_X = columnsMapper(X_df, X_columns)
    X_encoded = convertX(X_df, mapper_X)
    
    mapper_y = columnsMapper(pd.DataFrame({y_column: y_series}), [y_column])
    y_encoded = convertX(pd.DataFrame({y_column: y_series}), mapper_y)[y_column]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y_encoded, test_size=0.2, random_state=42
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    return model, mapper_X, mapper_y, accuracy


def persist_model(model, mapper_X, mapper_y, model_filename: str = 'car_model_predictor.joblib', 
                  mapper_filename: str = 'car_model_mappers.joblib'):
    joblib.dump(model, model_filename)
    print(f"Model saved to: {model_filename}")
    
    joblib.dump({'X': mapper_X, 'y': mapper_y}, mapper_filename)
    print(f"Mappers saved to: {mapper_filename}")


def get_hyundai_data(df: pd.DataFrame) -> pd.DataFrame:
    hyundai_df = df[df['Company'] == 'Hyundai'].copy()
    return hyundai_df


def get_toyota_expensive_data(df: pd.DataFrame, min_price: int = 40000) -> pd.DataFrame:
    toyota_expensive_df = df[(df['Company'] == 'Toyota') & (df['Price'] > min_price)].copy()
    return toyota_expensive_df


def get_top_models(df: pd.DataFrame, top_n: int = 3) -> pd.Series:
    model_counts = df['Model'].value_counts()
    top_models = model_counts.head(top_n)
    return top_models


def main():
    df = pd.read_csv('car_sales_data.csv')
    
    print("=" * 60)
    print("HW#30: Creating predictions model and working with pandas")
    print("=" * 60)
    
    print("\n1. Creating prediction model")
    print("-" * 60)
    
    X_columns = ['Gender', 'Color']
    y_column = 'Model'
    
    model, mapper_X, mapper_y, accuracy = create_prediction_model(df, X_columns, y_column)
    
    print("\n2. Persisting model")
    print("-" * 60)
    persist_model(model, mapper_X, mapper_y)
    
    print("\n3. Working with pandas")
    print("-" * 60)
    
    hyundai_df = get_hyundai_data(df)
    print(f"\nDataFrame containing only Hyundai data:")
    print(f"Number of rows: {len(hyundai_df)}")
    print(f"\nFirst 5 rows:")
    print(hyundai_df.head())
    
    toyota_expensive_df = get_toyota_expensive_data(df)
    print(f"\nDataFrame containing only Toyota with price > 40000:")
    print(f"Number of rows: {len(toyota_expensive_df)}")
    print(f"\nFirst 5 rows:")
    print(toyota_expensive_df.head())
    
    top_3_models = get_top_models(df, top_n=3)
    print(f"\n3 most popular car models:")
    for model_name, count in top_3_models.items():
        print(f"  {model_name}: {count} occurrences")
    
    print("\n" + "=" * 60)
    print("All tasks completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
