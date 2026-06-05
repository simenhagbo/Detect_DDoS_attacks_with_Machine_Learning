# Prosjektplan – ML-basert deteksjon av nettverksangrep

> Levende dokument. Oppdatert 5. juni 2026 etter gjennomgang (se `GJENNOMGANG-2026-06-05.md`).
> **Langsiktig mål:** en modell som kan overvåke eget nett/maskin og flagge ondsinnet trafikk.
> **Læringsmål:** forstå hvordan ML-modeller bygges inn mot cybersikkerhet, som forberedelse til studiet høsten 2026.

## Mål og rammer

- **Fase A (nå):** generell angrepsdeteksjon på CIC-IDS2017 – fler-angreps-trening og ærlig generaliseringsevaluering (leave-one-attack-out).
- **Fase B (senere):** anomalideteksjon på egen trafikk – egen benign baseline, ingen labels.
- **Fase C (til slutt):** live-pipeline på egen maskin + modne verktøy (Suricata) ved siden av.
- **Suksesskriterium:** ikke score på kjent data, men målt evne på *usette* angrep og realistisk falsk alarm-rate.

## Status

- [x] Fase 1: Datautforsking (`friday_ddos.csv`: 225 745 × 79, ~57/43 DDoS/BENIGN)
- [x] Fase 2: Rensing → `Data/Cleaned_data/friday_ddos_clean.csv` (223 082 × 68)
- [x] Fase 3: Forberedelse (80/20 stratifisert, 67 features, target aldri i X)
- [x] Fase 4: Baseline Random Forest (CPU)
- [x] Fase 5: Evaluering – nær perfekt på fredagsdata, **men**: gjennomgang beviste at modellen er LOIC-spesifikk (≈0 % recall på onsdagens DoS-verktøy). Ingen lekkasje – men evalueringen målte memorering av ett verktøy, ikke deteksjonsevne.
- [ ] **Etappe A** – generalisering med data vi har (pågår, se under)
- [ ] **Etappe B** – egen trafikk og anomalideteksjon
- [ ] **Etappe C** – live-pipeline + Suricata

---

## Hovedfunn fra gjennomgangen (premiss for alt videre)

1. **[HØY] Modellen er en LOIC-detektor, ikke en DDoS-detektor.** Trent på fredag, fanger den ~0 % av onsdagens DoS (Hulk 0,07 %, GoldenEye/slowloris/Slowhttptest 0,00 %). Nær-perfekte tall på fredag overselger den kraftig.
2. **[MEDIUM] Datadrevet kolonnedropp gir kolonnedrift.** Konstant-kolonne-identifisering per fil kan gi ulike kolonnesett per fil. Løsning: persistér trenings-feature-lista og reindekser nye filer mot den.
3. **[MEDIUM] `model.py` mangler evalueringsblokken** – fase 5-tallene er ikke reproduserbare fra koden i repoet.
4. **[LAV] Robusthet:** hardkodede relative stier, `drop` uten `errors='ignore'`, ubrukt import, ingen majoritets-baseline, ingen CV, modell lagres ikke.
5. **DestinationPort: avkreftet som problem** (fjerning flyttet FN 1→4; rank 12 i importance).

---

## Etappe A – generalisering med data vi HAR (gjør nå)

Læringspoeng: dette er selve ferdigheten – ærlig evaluering av generalisering.

### A0 – Rydd opp (fra gjennomgangen)
- Fullfør evalueringen i `model.py` (confusion matrix, P/R/F1, ROC-AUC på `predict_proba`, feature importance) så tallene er reproduserbare.
- Robusthet: `Path(__file__)`-stier, `errors='ignore'` på kolonnedropp, fjern ubrukt import.
- Legg til majoritets-baseline som referansepunkt. Lagre modell med `joblib`.

### A1 – Persistér feature-schema
- Lagre den eksakte trenings-kolonnelista (f.eks. JSON) ved trening.
- Alle nye filer reindekseres mot denne lista – aldri re-utled struktur per fil.

### A2 – Bygg fler-angreps-datasett
- Slå sammen: fredag DDoS (LOIC) + onsdag DoS (Hulk, GoldenEye, slowloris, Slowhttptest) + bred benign (mandag + flere dager).
- Samme renseflyt, men med schema fra A1.
- Først binær (BENIGN vs. ANGREP). Multiklasse (hvilket verktøy) som valgfri utvidelse.
- OBS: nå blir klassebalansen skjev (mye mer benign) – vurder class weights / terskeljustering, og mål precision/recall fremfor accuracy.

### A3 – Leave-one-attack-out-evaluering (den ekte testen)
- Tren på alle verktøy unntatt ett, test på det utholdte (f.eks. hold Slowhttptest utenfor).
- Mål: recall på det usette verktøyet + falsk alarm-rate på benign.
- Roter gjerne hvilket verktøy som holdes ute.
- Åpent spørsmål fra gjennomgangen: generaliserer fredag+onsdag-modellen til et fjerde verktøy?

### A4 – Datakvalitet
- CIC-IDS2017 har dokumenterte label-/feature-feil (Engelen et al. 2021, «Troubleshooting an Intrusion Detection Dataset»). Det finnes en korrigert versjon (DistriNet/KU Leuven).
- Vit om dette før tallene tolkes som fasit; vurder å bytte til korrigerte CSV-er.

**Leveranse Etappe A:** en fler-angreps-modell med ærlig målt generalisering, reproduserbar pipeline med fast feature-schema.

## Etappe B – egen trafikk og anomalideteksjon

Problemtypen skifter: fra klassifisering (labels finnes) til anomalideteksjon (ingen labels på eget nett).

- **B1 – Egen benign baseline:** kjør flow-eksportør på eget nett i dager/uker. Kandidater: nfstream (Python, CIC-lignende features), Zeek, CICFlowMeter. Valget styres av feature-paritet med treningen.
- **B2 – Anomalimodell:** tren på egen normaltrafikk (Isolation Forest, One-Class SVM, autoencoder). Flagg avvik – ikke klassifiser angrepstype.
- **B3 – Realistisk falsk alarm-måling:** base-rate-realiteten (Axelssons base-rate fallacy): med hundretusener av flows/dag gir selv 0,07 % FP hundrevis av daglige falske alarmer. Konsekvens: modellen er **triage/rangering**, aldri auto-blokkering. Mål FP per dag, ikke bare prosent.

## Etappe C – live-pipeline og produksjonskontekst

- **C1 – Pipeline:** pakkefangst → flow-features (identiske med trening – bruk schemaet fra A1) → modell → varsling. Egen ingeniørjobb.
- **C2 – Modne verktøy ved siden av:** Suricata/Snort (signatur-IDS) for kjente angrep, Zeek for analyse. Realistisk arkitektur: Suricata i bunn + eget ML-anomalilag for det ukjente. Suricata fungerer også som «fasit» å sammenligne ML-laget mot.
- Ærlig ramme: for faktisk beskyttelse er modne verktøy bedre enn egen modell. ML-delen bygges som læringsvehikkel – og for å forstå hvor den hører hjemme.

---

## Historikk: Fase 1–5 (fullført, fredagsfila)

### Fase 1 – EDA ✓
225 745 × 79; 65 kolonnenavn med mellomrom (inkl. `" Label"`); 34 inf-rader; 4 NaN; 2 633 duplikater; 10 konstante kolonner; duplisert `Fwd Header Length` (pandas: `.1`).

### Fase 2 – Rensing ✓
Rekkefølge: kolonnenavn → konstante kolonner + dublett → duplikate rader → inf→NaN → dropp NaN-rader → verifiser → lagre (uten indeks, aldri over råfila). Resultat: 223 082 × 68.

### Fase 3 – Forberedelse ✓
Binær target (DDoS=1), X/y-splitt, 80/20 stratifisert, fast frø. Skalering utsatt (per modell senere).

### Fase 4 – Baseline ✓
Random Forest, standardinnstillinger, fast frø, CPU (< 1 min).

### Fase 5 – Evaluering ✓ (med forbehold)
FN=1, FP=0, ROC-AUC ~1.0 på fredag. Verifisert: ingen lekkasje, ingen snarvei-feature (høyeste univariate AUC 0,80). **Men:** gjelder kun LOIC + fredags-benign. Se hovedfunn 1.

---

## Tekniske notater

- **Stier:** bruk `Path(__file__).parent` – aldri avhengig av cwd.
- **Feature-schema:** trenings-kolonnelista er sannheten; nye filer reindekseres mot den (hovedfunn 2).
- **Skalering:** per modell, kun tilpasset på treningsdata. RF trenger ikke; LogReg/SVM/autoencoder gjør.
- **ROC-AUC:** alltid på sannsynligheter (`predict_proba`), ikke 0/1-prediksjoner.
- **Klassebalanse:** fredagsfila var ~57/43; det sammenslåtte datasettet blir sterkt benign-dominert → class weights/terskler + precision/recall-fokus.
- **GPU:** WSL2 + RAPIDS klart (se `GPU_SETUP.md`); lønner seg først ved tuning/store data. CPU på Windows-siden ellers.
- **Duplikater:** nesten alle fjernede rader var BENIGN; DDoS falt bare 13 (128 027 → 128 014).
- **DestinationPort:** beholdt; avkreftet som snarvei (gjennomgangen).
