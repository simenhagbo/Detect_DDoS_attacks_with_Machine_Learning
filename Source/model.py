import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import time

# Last inn datasettet
df = pd.read_csv("Data/Cleaned_data/friday_ddos_clean.csv")

# Map hva som skal enkodes
mapping = {'BENIGN' : 0, 'DDoS' : 1}

# Oppretter ny kolonne
df['target'] = df['Label'].map(mapping)
print(df['target'].value_counts())

# Split datasettet i X og y
X = df.drop(columns=['Label', 'target'], errors='ignore')
y = df['target']

# Split i train og test sett
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

# Oppretter en baseline RF Classifier
baseline_rf = RandomForestClassifier(random_state=1, n_jobs=-1)

print("Starter trening av Random Forest baseline...")
start_tid = time.time()

# Tren modellen
baseline_rf.fit(X_train, y_train)

slutt_tid = time.time()
print(f"Trening fullført på {slutt_tid - start_tid:.2f} sekunder.")

# Prediker på testsettet
y_pred = baseline_rf.predict(X_test)

# Hent sannsynlighet for den positive klassen (DDoS)
y_probs = baseline_rf.predict_proba(X_test)[:, 1]