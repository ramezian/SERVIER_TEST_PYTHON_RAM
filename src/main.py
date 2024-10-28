from src.data_ingestion.load_data import load_csv, load_json
from src.data_processing.cleaning import (
    clean_json_file, standardize_date_format, convert_id_to_string, rename_columns,
    fill_missing_numeric_ids, sanitize_title_text, remove_rows_with_empty_titles_or_journals,
    remove_duplicate_ids_and_reindex, remove_rows_with_empty_id
)
from src.data_processing.processing import build_drug_mentions_graph
from src.data_export.export_json import export_to_json
from src import config
import os

# Créer le dossier de sortie si nécessaire
os.makedirs(config.LINK_GRAPH_DIR, exist_ok=True)

def main():
    # Nettoyer le fichier JSON et le sauvegarder dans Preparation
    clean_json_file(config.SRC_PUBMED_JSON_FILE_PATH, config.PUBMED_JSON_FILE_PATH)

    # Charger les fichiers CSV sources
    drugs_df = load_csv(config.SRC_DRUGS_FILE_PATH)
    pubmed_df = load_csv(config.SRC_PUBMED_FILE_PATH)
    clinical_trials_df = load_csv(config.SRC_CLINICAL_TRIALS_FILE_PATH)

    # Nettoyer les données
    print("Nettoyage des données...")

    # Convertir les IDs en chaînes de caractères et retirer les doublons
    drugs_df = convert_id_to_string(drugs_df, 'atccode')
    drugs_df = remove_duplicate_ids_and_reindex(drugs_df, 'atccode')
    drugs_df.to_csv(config.DRUGS_FILE_PATH, index=False)  # Sauvegarder dans Preparation
    
    # Charger le fichier JSON nettoyé
    pubmed_json_df = load_json(config.PUBMED_JSON_FILE_PATH)
    pubmed_df = standardize_date_format(pubmed_df, 'date')
    clinical_trials_df = standardize_date_format(clinical_trials_df, 'date')

    # Nettoyage supplémentaire pour éviter les données vides ou non valides
    pubmed_df = sanitize_title_text(pubmed_df, 'title')
    clinical_trials_df = sanitize_title_text(clinical_trials_df, 'scientific_title')
    pubmed_df = remove_rows_with_empty_titles_or_journals(pubmed_df, 'title', 'journal')
    clinical_trials_df = remove_rows_with_empty_titles_or_journals(clinical_trials_df, 'scientific_title', 'journal')
    pubmed_df = remove_duplicate_ids_and_reindex(pubmed_df, 'id')
    clinical_trials_df = remove_duplicate_ids_and_reindex(clinical_trials_df, 'id')
    
    # Sauvegarder les données nettoyées dans Preparation
    pubmed_df.to_csv(config.PUBMED_FILE_PATH, index=False)
    clinical_trials_df.to_csv(config.CLINICAL_TRIALS_FILE_PATH, index=False)

    # Charger les données nettoyées pour la construction du graphe
    print("Construction du graphe de liaison...")
    graph_data = build_drug_mentions_graph(drugs_df, pubmed_df, clinical_trials_df)

    # Vérifier si graph_data est non vide
    if graph_data:
        # Exporter le graphe vers un fichier JSON
        export_to_json(graph_data, config.OUTPUT_JSON_PATH)
        print(f"Exportation réussie du fichier JSON dans {config.OUTPUT_JSON_PATH}.")
    else:
        print("Erreur : Aucun contenu dans le graphe à exporter.")

if __name__ == "__main__":
    main()
