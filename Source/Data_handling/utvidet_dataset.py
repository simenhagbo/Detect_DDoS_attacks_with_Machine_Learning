import pandas as pd
import numpy as np
from pathlib import Path

# Hent datasettet
data_mappe = Path(r"C:\Users\simen\Mine Sommerprosjekter\Detect DDoS Attacks ML-model\Data\CSV_files")
target_filer = {"friday_ddos.csv", "wednsday_dos.csv", "monday_benign.csv"}
fil_liste = []

# Iterer gjennom mapen og legg de aktuelle filene inn i fil_liste
for fil in data_mappe.iterdir():
    # Sjekk at elementet faktisk er en fil og legg til i fil_listen
    if fil.is_file() and fil.name in target_filer:
        fil_liste.append(fil)
print("Fil listen: ", fil_liste)

# Liste med DataFrames
df_liste = []
# Les, rens og legg filene i listen med dataframes
for fil in fil_liste:
    print(f"Leser inn {fil.name}...")
    df = pd.read_csv(fil)
    df.columns = df.columns.str.replace(" ", "")
    df_liste.append(df)

# Slå sammen alle dataframes til en dataframe
samlet_df = pd.concat(df_liste, ignore_index=True)

# Sjekk shape
print("Shape før rensing: ", samlet_df.shape)

# Identifiser konstante kolonner
konstante_kolonner = [col for col in samlet_df.columns if samlet_df[col].nunique() == 1]

# Rens det utvidede datasettet
samlet_df = samlet_df.drop(konstante_kolonner, axis=1)
samlet_df = samlet_df.drop(["FwdHeaderLength.1"], axis=1, errors='ignore')
samlet_df = samlet_df.drop_duplicates()

# Konverter inf verdier til nan
samlet_df = samlet_df.replace([np.inf, -np.inf], np.nan)
# Dropper nan verdier
samlet_df = samlet_df.dropna()

print("Shape etter rensing: ", samlet_df.shape)