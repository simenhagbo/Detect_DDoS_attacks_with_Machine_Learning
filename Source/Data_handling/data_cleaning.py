import pandas as pd
import numpy as np
from pathlib import Path

# Les data inn til pandas dataframe
df_original = pd.read_csv("Data\CSV_files\friday_ddos.csv")
df = df_original.copy()

# Fjern mellomrom fra alle kolonnenavn
df.columns = df.columns.str.replace(" ", "")

# Identifiser konstante kolonner
konstante_kolonner = [col for col in df.columns if df[col].nunique() == 1]

# Behold kun kolonner med mer enn 1 unik verdi
df = df.drop(konstante_kolonner, axis=1)
# Fjern FwdHeaderLength.1 kolonnen
df = df.drop(['FwdHeaderLength.1'], axis=1)
# Fjern duplikater
df = df.drop_duplicates()

# Konverter inf verdier til nan verdier
df = df.replace([np.inf, -np.inf], np.nan)


# Dropp rader med nan verdier
df = df.dropna()

nan_verdier = df.isna().sum()
kolonner_m_nan = nan_verdier[nan_verdier > 0]
print(kolonner_m_nan)

# Sjekk datasettet etter rensing
print(df.info())

# Sjekk for gjenværende inf verdier
inf_teller = np.isinf(df.select_dtypes(include=np.number)).sum().sum()
print("Gjenværende inf verdier: ", inf_teller)

# Sjekk for gjenværende duplicaater
dup_teller = df.duplicated().sum()
print("Gjenværende duplikater: ", dup_teller)

# Erstatt 'Label' med det faktiske navnet  på målvariabel klassen
print("Antall per klasse")
print(df['Label'].value_counts())

print("Prosentvis fordeling")
print(df['Label'].value_counts(normalize=True) * 100)

# Sjekk nåværende shape etter drop
print(df.shape)

# Lagre renset dataset til en ny fil
df.to_csv("Data/Cleaned_data/friday_ddos_clean.csv", index=False)