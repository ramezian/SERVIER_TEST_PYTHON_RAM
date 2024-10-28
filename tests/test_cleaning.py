import pandas as pd
from src.data_processing.cleaning import (
    standardize_date_format, convert_id_to_string, rename_columns,
    fill_missing_numeric_ids, sanitize_title_text, remove_rows_with_empty_titles_or_journals,
    remove_duplicate_ids_and_reindex, replace_nan_with_empty_string
)

def test_standardize_date_format():
    df = pd.DataFrame({'date': ['2024-10-01', '01/10/2024', '2024.10.01']})
    df = standardize_date_format(df, 'date')
    assert all(df['date'].str.match(r'\d{4}-\d{2}-\d{2}'))

def test_convert_id_to_string():
    df = pd.DataFrame({'id': [123, 456, 789]})
    df = convert_id_to_string(df, 'id')
    assert df['id'].dtype == object

def test_replace_nan_with_empty_string():
    df = pd.DataFrame({'col': [1, None, 'test']})
    df = replace_nan_with_empty_string(df)
    assert df['col'].isnull().sum() == 0
