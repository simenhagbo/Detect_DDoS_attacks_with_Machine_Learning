import pandas as pd
from pathlib import Path

# Konfiguer
mappe_sti = Path(r"C:\Users\simen\Mine Sommerprosjekter\Detect DDoS Attacks ML-model\Data\CSV_files")


for fil in mappe_sti.glob("*.csv"):
    # Les filen
    df = pd.read_csv(fil)
    print(f"Sjekker {fil.name}..")
    print(f"Shape på datasattet: {df.shape}")

    # Tell opp labels ved å sjekke strengen direkte
    if "Label" in df.columns:
        print(df['Label'].value_counts().to_string())
    elif " Label" in df.columns:
        print(df[' Label'].value_counts().to_string())
    else:
        print("Fant ingen label-kolonne.")