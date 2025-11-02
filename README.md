# HW #29 Definition

## Write module (Python file 'converter.py') containing the following functions

### def enumerator(values: Iterable[str]) -> dict[str, int]

takes Iterable of strings  
returns dictionary with initial string as key and sequentianal number as value  
hint: use dictionary comprehension expression with enumerating

### def columnsMapper(columnsStr: list[str], df: DataFrame)->dict[str, dict[str, int]]

takes list of the column names DataFrame (type from pandas; if there is 'import pandas as pd' this type may be defined like pd.DataFrame)  
returns dictionary with name of column as key and dictionary (see description of returning type in previous function) as value  
this function is intended for getting enumerated values for the specified columns

### def convertX(df:pd.DataFrame, mapper: dict[str, dict[str, int]])-> pd.DataFrame

takes DataFrame and mapper (result of the previous function)  
returns DataFrame with columns containing sequentianal numbers as the values  
this function is intended for converting DataFrame containing strings as the values to a DataFrame containing the numbers as the values

## Write test_converter.py module with the tests

### Notes

1. Creating DataFrame example with test result: df = pd.DataFrame({"Company":['Toyota','Toyota','Hundai', 'Hundai', 'Hundai' ], "Model": ['Camry', 'Corolla', 'i10', 'Elantra', 'Kona']}); dfConverted = convertX(df, mapper={'Company': {'Toyota': 0, 'Hundai': 1}, 'Model': {'Camry': 0, 'Corolla': 1, 'i10': 2, 'Elantra':3, 'Kona':4}}); dfConverter.to_dict(orient="list") will be {"Company":[0,0,1,1,1], "Model": [0, 1, 2, 3, 4]}  
Note: dfConverter.to_dict(orient="list") the method of converting DataFrame to a dictionary in the specified above format for testing

## Files

- `converter.py` - implementation of converter module with enumerator, columnsMapper, and convertX functions
- `test_converter.py` - tests for converter module
