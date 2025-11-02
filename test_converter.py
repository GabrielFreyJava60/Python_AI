import pandas as pd
from converter import enumerator, columnsMapper, convertX


def test_enumerator():
    values = ['Toyota', 'Hundai']
    result = enumerator(values)
    assert result == {'Toyota': 0, 'Hundai': 1}, f"Expected {{'Toyota': 0, 'Hundai': 1}}, got {result}"
    
    values2 = ['Camry', 'Corolla', 'i10', 'Elantra', 'Kona']
    result2 = enumerator(values2)
    assert result2 == {'Camry': 0, 'Corolla': 1, 'i10': 2, 'Elantra': 3, 'Kona': 4}, \
        f"Expected enumerated dict, got {result2}"
    
    values3 = ['A', 'B', 'A', 'C']
    result3 = enumerator(values3)
    assert len(result3) == 3
    assert result3['A'] == 2
    assert result3['B'] == 1
    assert result3['C'] == 3
    
    print("✓ test_enumerator passed")


def test_columnsMapper():
    df = pd.DataFrame({
        "Company": ['Toyota', 'Toyota', 'Hundai', 'Hundai', 'Hundai'],
        "Model": ['Camry', 'Corolla', 'i10', 'Elantra', 'Kona']
    })
    
    result = columnsMapper(["Company", "Model"], df)
    
    assert "Company" in result, "Company should be in result"
    assert "Model" in result, "Model should be in result"
    
    assert result["Company"] == {'Toyota': 0, 'Hundai': 1}, \
        f"Company mapping incorrect: {result['Company']}"
    
    assert result["Model"] == {'Camry': 0, 'Corolla': 1, 'i10': 2, 'Elantra': 3, 'Kona': 4}, \
        f"Model mapping incorrect: {result['Model']}"
    
    result2 = columnsMapper(["Company"], df)
    assert len(result2) == 1
    assert "Company" in result2
    
    print("✓ test_columnsMapper passed")


def test_convertX():
    df = pd.DataFrame({
        "Company": ['Toyota', 'Toyota', 'Hundai', 'Hundai', 'Hundai'],
        "Model": ['Camry', 'Corolla', 'i10', 'Elantra', 'Kona']
    })
    
    mapper = {
        'Company': {'Toyota': 0, 'Hundai': 1},
        'Model': {'Camry': 0, 'Corolla': 1, 'i10': 2, 'Elantra': 3, 'Kona': 4}
    }
    
    dfConverted = convertX(df, mapper)
    result_dict = dfConverted.to_dict(orient="list")
    
    expected = {"Company": [0, 0, 1, 1, 1], "Model": [0, 1, 2, 3, 4]}
    assert result_dict == expected, \
        f"Expected {expected}, got {result_dict}"
    
    assert dfConverted['Company'].dtype in [int, 'int64', 'int32'], \
        f"Company column should be integer, got {dfConverted['Company'].dtype}"
    assert dfConverted['Model'].dtype in [int, 'int64', 'int32'], \
        f"Model column should be integer, got {dfConverted['Model'].dtype}"
    
    print("✓ test_convertX passed")


def test_integration():
    df = pd.DataFrame({
        "Company": ['Toyota', 'Toyota', 'Hundai', 'Hundai', 'Hundai'],
        "Model": ['Camry', 'Corolla', 'i10', 'Elantra', 'Kona']
    })
    
    mapper = columnsMapper(["Company", "Model"], df)
    
    dfConverted = convertX(df, mapper)
    result_dict = dfConverted.to_dict(orient="list")
    
    expected = {"Company": [0, 0, 1, 1, 1], "Model": [0, 1, 2, 3, 4]}
    assert result_dict == expected, \
        f"Integration test failed: Expected {expected}, got {result_dict}"
    
    print("✓ test_integration passed")


def test_enumerator_edge_cases():
    result = enumerator([])
    assert result == {}, f"Empty iterable should return empty dict, got {result}"
    
    result = enumerator(['Single'])
    assert result == {'Single': 0}, f"Single value should be 0, got {result}"
    
    print("✓ test_enumerator_edge_cases passed")


def test_convertX_partial_mapping():
    df = pd.DataFrame({
        "Company": ['Toyota', 'Toyota', 'Hundai'],
        "Model": ['Camry', 'Corolla', 'i10'],
        "Year": [2020, 2021, 2022]
    })
    
    mapper = {
        'Company': {'Toyota': 0, 'Hundai': 1}
    }
    
    dfConverted = convertX(df, mapper)
    
    assert dfConverted['Company'].tolist() == [0, 0, 1]
    
    assert dfConverted['Model'].tolist() == ['Camry', 'Corolla', 'i10']
    assert dfConverted['Year'].tolist() == [2020, 2021, 2022]
    
    print("✓ test_convertX_partial_mapping passed")


if __name__ == "__main__":
    print("Running converter tests...\n")
    
    test_enumerator()
    test_columnsMapper()
    test_convertX()
    test_integration()
    test_enumerator_edge_cases()
    test_convertX_partial_mapping()
    
    print("\n✅ All tests passed!")

