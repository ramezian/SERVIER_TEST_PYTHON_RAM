import json
import os
from src.data_export.export_json import export_to_json
from src import config

def test_export_to_json():
    data = {'test': 'value'}
    output_path = 'tests/test_output.json'
    export_to_json(data, output_path)
    assert os.path.exists(output_path)

    with open(output_path, 'r') as file:
        loaded_data = json.load(file)
    assert loaded_data == data

    os.remove(output_path)
