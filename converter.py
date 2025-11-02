from typing import Iterable
import pandas as pd


def enumerator(values: Iterable[str]) -> dict[str, int]:
    return {value: idx for idx, value in enumerate(values)}


def columnsMapper(df: pd.DataFrame, columnsStr: list[str]) -> dict[str, dict[str, int]]:
    result = {}
    for column in columnsStr:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        unique_values = df[column].unique()
        result[column] = enumerator(unique_values)
    return result


def convertX(df: pd.DataFrame, mapper: dict[str, dict[str, int]]) -> pd.DataFrame:
    result_df = df.copy()
    for column, mapping_dict in mapper.items():
        if column in result_df.columns:
            result_df[column] = result_df[column].map(mapping_dict)
    return result_df

