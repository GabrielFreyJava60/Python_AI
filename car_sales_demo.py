from main import RandomNumbersStream
import csv
from typing import Optional


class CarSalesData:
    def __init__(self, csv_file: str):
        self.records = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.records.append(row)
    
    def get_record(self, index: int) -> Optional[dict]:
        if 0 <= index < len(self.records):
            return self.records[index]
        return None
    
    def __len__(self) -> int:
        return len(self.records)
    
    def print_record(self, record: dict) -> None:
        print(f"  Gender: {record['Gender']}, "
              f"Income: ${record['Annual Income']:>12}, "
              f"{record['Company']} {record['Model']}, "
              f"Price: ${record['Price ($)']}")


print("=== Car Sales Data with RandomNumbersStream ===\n")

car_data = CarSalesData('car_sales_cleaned1.csv')
print(f"Total records in CSV: {len(car_data)}\n")

print("1. Random car selection (10 cars):")
stream = RandomNumbersStream(min=0, max=len(car_data) - 1)
stream.setLimit(10)
for idx in stream:
    record = car_data.get_record(idx)
    if record:
        car_data.print_record(record)

print("\n2. Random expensive cars (price > 40000):")
price_filter_stream = RandomNumbersStream(min=0, max=len(car_data) - 1)
price_filter_stream.setFilter(lambda idx: car_data.get_record(idx) and int(car_data.get_record(idx).get('Price ($)', 0)) > 40000)
price_filter_stream.setLimit(5)
print("   Finding 5 expensive cars...")
for idx in price_filter_stream:
    record = car_data.get_record(idx)
    if record:
        car_data.print_record(record)

print("\n3. Unique random indices (first 20 unique records):")
unique_stream = RandomNumbersStream(min=0, max=len(car_data) - 1)
unique_stream.setDistinct()
unique_stream.setLimit(20)
for idx in unique_stream:
    record = car_data.get_record(idx)
    if record:
        print(f"  Index {idx}: {record['Company']} {record['Model']} - ${record['Price ($)']}")

print("\n4. Random cars with high income buyers (income > 1000000):")
high_income_stream = RandomNumbersStream(min=0, max=len(car_data) - 1)
high_income_stream.setFilter(lambda idx: car_data.get_record(idx) and int(car_data.get_record(idx).get('Annual Income', 0)) > 1000000)
high_income_stream.setLimit(5)
for idx in high_income_stream:
    record = car_data.get_record(idx)
    if record:
        car_data.print_record(record)

print("\n5. Random BMW cars:")
bmw_stream = RandomNumbersStream(min=0, max=len(car_data) - 1)
bmw_stream.setFilter(lambda idx: car_data.get_record(idx) and car_data.get_record(idx).get('Company') == 'BMW')
bmw_stream.setLimit(5)
for idx in bmw_stream:
    record = car_data.get_record(idx)
    if record:
        car_data.print_record(record)

