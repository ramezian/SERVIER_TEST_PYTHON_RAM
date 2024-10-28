import os
import pandas as pd
from src.data_ingestion.load_data import load_csv, load_json
from src import config

def test_load_csv():
    df = load_csv(config.SRC_DRUGS_FILE_PATH)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'atccode' in df.columns

def test_load_json():
    data = load_json(config.PUBMED_JSON_FILE_PATH)
    assert isinstance(data, pd.DataFrame) 
    assert not data.empty
    assert 'id' in data.columns