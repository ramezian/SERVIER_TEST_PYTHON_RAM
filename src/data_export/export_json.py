import json
from typing import Dict
def export_to_json(data: dict, output_path: str):
    if data:
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Exportation réussie du fichier JSON dans {output_path}.")
    else:
        print("Erreur : Aucun contenu à exporter dans link_graph.json.")
