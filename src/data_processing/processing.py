import pandas as pd
import re
from typing import Dict

def build_drug_mentions_graph(drugs_df, pubmed_df, clinical_trials_df):
    graph_data = {}
    
    for _, drug_row in drugs_df.iterrows():
        drug = drug_row['drug']
        mentions = []

        
        for _, row in pubmed_df.iterrows():
            title = row.get('title', '')
            date = row.get('date', '')

            
            date = date if pd.notna(date) else ""
            
            if isinstance(title, str) and re.search(rf'\b{drug}\b', title, re.IGNORECASE):
                mentions.append({
                    'source': 'pubmed',
                    'id': row['id'],
                    'title': title,
                    'journal': row['journal'],
                    'date': date
                })

        
        for _, row in clinical_trials_df.iterrows():
            scientific_title = row.get('scientific_title', '')
            date = row.get('date', '')

          
            date = date if pd.notna(date) else ""

            if isinstance(scientific_title, str) and re.search(rf'\b{drug}\b', scientific_title, re.IGNORECASE):
                mentions.append({
                    'source': 'clinical_trials',
                    'id': row['id'],
                    'title': scientific_title,
                    'journal': row['journal'],
                    'date': date
                })

        if mentions:
            graph_data[drug] = mentions

    return graph_data
