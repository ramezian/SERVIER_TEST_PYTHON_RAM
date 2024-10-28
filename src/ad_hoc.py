import json
from collections import Counter
from src import config

def export_most_mentioned_journal():
    # Charger les données du graphe de mentions
    try:
        with open(config.OUTPUT_JSON_PATH, 'r') as file:
            data = json.load(file)
        print("Contenu de drug_mentions_graph.json chargé avec succès.")
    except json.JSONDecodeError as e:
        print("Erreur lors du chargement de drug_mentions_graph.json:", e)
        return
    
    # Vérifier le contenu des données chargées
    if not data:
        print("Aucune donnée trouvée dans drug_mentions_graph.json.")
        return
    
    print("Données chargées:", data)

    # Compteur pour le nombre de mentions par journal
    journal_counter = Counter()

    # Parcourir les mentions de chaque médicament pour compter les journaux
    for mentions in data.values():
        unique_journals = set([mention["journal"] for mention in mentions if mention.get("journal")])
        for journal in unique_journals:
            journal_counter[journal] += 1
    
    # Vérifier le contenu du compteur de journaux
    print("Compteur des journaux:", journal_counter)

    # Trouver le journal avec le plus de mentions
    most_mentioned_journal = journal_counter.most_common(1)
    if most_mentioned_journal:
        result = {
            "journal": most_mentioned_journal[0][0],
            "mentions": most_mentioned_journal[0][1]
        }
    else:
        result = {"journal": "No journal found", "mentions": 0}

    # Sauvegarder le résultat dans un fichier JSON
    with open(config.AD_HOC_OUTPUT_PATH, 'w') as file:
        json.dump(result, file, indent=4)

    print(f"Le fichier JSON du journal le plus mentionné a été exporté dans {config.AD_HOC_OUTPUT_PATH}.")

# Appeler la fonction pour générer le fichier ad-hoc
if __name__ == "__main__":
    export_most_mentioned_journal()
