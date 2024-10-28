import os
import json
from src.ad_hoc import export_most_mentioned_journal
from src import config

def test_export_most_mentioned_journal():
    # Utiliser un fichier test pour drug_mentions_graph.json
    test_data = {
        "DrugA": [{"journal": "Journal1"}, {"journal": "Journal2"}],
        "DrugB": [{"journal": "Journal1"}]
    }
    test_output_path = 'tests/test_most_mentioned_journal.json'
    with open(config.OUTPUT_JSON_PATH, 'w') as file:
        json.dump(test_data, file)

    # Appeler la fonction
    export_most_mentioned_journal()

    # Vérifier le fichier de sortie
    assert os.path.exists(config.AD_HOC_OUTPUT_PATH)
    with open(config.AD_HOC_OUTPUT_PATH, 'r') as file:
        result = json.load(file)
    assert result['journal'] == "Journal1"
    
    # Nettoyer les fichiers de test
    os.remove(config.OUTPUT_JSON_PATH)
    os.remove(config.AD_HOC_OUTPUT_PATH)
