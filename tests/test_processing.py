from src.data_processing.processing import build_drug_mentions_graph
import pandas as pd

def test_build_drug_mentions_graph():
    drugs_df = pd.DataFrame({'drug': ['Aspirin']})
    pubmed_df = pd.DataFrame({'title': ['Aspirin is effective'], 'journal': ['Journal1'], 'date': ['2021-01-01'], 'id': [1]})
    clinical_trials_df = pd.DataFrame({'scientific_title': ['Aspirin trial'], 'journal': ['Journal2'], 'date': ['2021-02-01'], 'id': [2]})
    
    graph = build_drug_mentions_graph(drugs_df, pubmed_df, clinical_trials_df)
    assert 'Aspirin' in graph
    assert len(graph['Aspirin']) == 2  # Vérifier que les deux mentions sont trouvées
