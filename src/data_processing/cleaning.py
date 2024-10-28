import pandas as pd
import json
import re

def clean_json_file(input_path: str, output_path: str) -> None:
    
    
    
    try:
       
        with open(input_path, 'r') as file:
            data = json.load(file)
        
        
        cleaned_data = [item for item in data if item.get("id") != ""]

        
        with open(output_path, 'w') as file:
            json.dump(cleaned_data, file, indent=4)
        
        print(f"Le fichier JSON a été nettoyé et sauvegardé dans {output_path}.")
    
    except json.JSONDecodeError as e:
        print(f"Erreur JSON détectée : {e}. Tentative de nettoyage en mode texte...")

        with open(input_path, 'r') as file:
            raw_text = file.read()

        # 1. Ajouter des guillemets autour des clés JSON sans guillemets
        corrected_text = re.sub(r'(?<!")(\b\w+\b)(?!")(?=\s*:)', r'"\1"', raw_text)

        # 2. Retirer les virgules en trop avant les accolades et crochets fermants
        corrected_text = re.sub(r',\s*([\]}])', r'\1', corrected_text)

        # 3. Encapsuler en une liste JSON si nécessaire
        if not corrected_text.strip().startswith("["):
            corrected_text = f"[{corrected_text.strip()}]"

        # Charger et filtrer les objets après correction du format
        try:
            corrected_data = json.loads(corrected_text)
            cleaned_data = [item for item in corrected_data if item.get("id") != ""]
            
            # Sauvegarder le JSON nettoyé sans les éléments "id" vides
            with open(output_path, 'w') as file:
                json.dump(cleaned_data, file, indent=4)
            
            print(f"Le fichier JSON a été nettoyé et sauvegardé dans {output_path}.")
        
        except json.JSONDecodeError as inner_e:
            print(f"Erreur de format persistante après tentative de nettoyage : {inner_e}")
    except Exception as ex:
        print(f"Une autre erreur est survenue : {ex}")

def standardize_date_format(df, date_column_name):
    # Convertir les dates, gérer les erreurs et formater explicitement en `YYYY-MM-DD`
    df[date_column_name] = pd.to_datetime(df[date_column_name], errors='coerce').dt.strftime('%Y-%m-%d')
    df[date_column_name] = df[date_column_name].replace("NaT", "")  
    return df
def convert_id_to_string(df, id_column_name):
    df[id_column_name] = df[id_column_name].astype(str)
    return df

def rename_columns(df, column_naming_mapping):
    return df.rename(columns=column_naming_mapping)

def fill_missing_numeric_ids(df, id_column_name):
    max_id = df[id_column_name].dropna().max()
    missing_ids_count = df[id_column_name].isna().sum()
    df.loc[df[id_column_name].isna(), id_column_name] = range(max_id + 1, max_id + missing_ids_count + 1)
    df[id_column_name] = df[id_column_name].astype(int)
    return df

def sanitize_title_text(df, title_column_name):
    df[title_column_name] = df[title_column_name].str.encode('ascii', 'ignore').str.decode('utf-8')
    df[title_column_name] = df[title_column_name].str.replace(r'[^\w\s-]', '', regex=True)
    df[title_column_name] = df[title_column_name].str.title().str.strip().str.replace(r'\s+', ' ', regex=True)
    return df

def remove_rows_with_empty_titles_or_journals(df, title_column_name, journal_column_name):
    return df.dropna(subset=[title_column_name, journal_column_name])

def remove_duplicate_ids_and_reindex(df, id_column_name):
       return df.drop_duplicates(subset=[id_column_name]).reset_index(drop=True)

def remove_rows_with_empty_id(df, id_column_name):
    
    return df.dropna(subset=[id_column_name])

def replace_nan_with_empty_string(df):
    
    return df.fillna("")