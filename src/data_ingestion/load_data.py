import pandas as pd
import json

def load_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def load_json(file_path: str) -> pd.DataFrame:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

