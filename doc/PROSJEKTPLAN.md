# Prosjektplan – ML-basert DDoS-deteksjon

> Synkronisert kopi per 5. juni 2026. Den levende versjonen ligger i arbeidsmappa: `doc/PLAN.md` i «Detect DDoS Attacs ML-model».
> Hovedmål: en fungerende ML-modell som detekterer DDoS-angrep, trent på CIC-IDS2017.
> Se også `CIC-IDS2017-dataset.md` (datasettkontekst) i denne mappa.

## Formål

Hovedformålet er **læring**: forstå hvordan man bygger ML-modeller rettet mot cybersikkerhet, som forberedelse til cybersikkerhetsstudiet høsten 2026. Simen skriver koden selv, steg for steg. Det ferdige produktet er sekundært til forståelsen.

## Mål og rammer

- **Oppgavetype:** Binær klassifisering – DDoS (1) vs. BENIGN (0).
- **Suksesskriterium:** Modell med høy recall på DDoS og lav andel falske alarmer, evaluert på data den ikke har sett.
- **Data:** CIC-IDS2017, hovedfil `friday_ddos.csv` (DDoS LOIT + benign, fredag ettermiddag).

## Status

- [x] Datasett lastet ned og lagt i `Data/CSV_files/`
- [x] Kontekstfil opprettet
- [x] Lasting av data verifisert (`(225745, 79)`)
- [x] Fase 1: Datautforsking
- [x] Fase 2: Rensing → `Data/Cleaned_data/friday_ddos_clean.csv` (223 082 × 68)
- [x] Fase 3: Forberedelse til modellering (80/20 stratifisert: 178 465 train / 44 617 test, 67 features)
- [x] Fase 4: Baseline-modell (Random Forest, CPU, < 1 min trening)
- [x] Fase 5: Evaluering (~perfekt: recall/precision/F1 = 1.00, 1 FN av 25 603 DDoS). Ingen lekkasje. Importance spredt på legitime flow-features; DestinationPort ikke i topp 10 → ingen snarvei.
- [ ] Fase 6: Forbedring og generalisering (eneste reelle test av om modellen er ekte god)

## Fasene

### Fase 1 – Datautforsking (EDA) ✓

Funn: 225 745 × 79; label-balanse ~57/43 (DDoS/BENIGN); 65 kolonnenavn med mellomrom (inkl. `" Label"`); 34 rader med inf; 4 NaN; 2 633 duplikater; 10 konstante kolonner; duplisert kolonne `Fwd Header Length` (pandas-omdøpt til `.1`).

### Fase 2 – Datarensing ✓

Rekkefølge: rydd kolonnenavn → identifiser og dropp konstante kolonner + dublettkolonnen → fjern duplikate rader → inf → NaN → dropp NaN-rader → verifiser → lagre rent datasett (uten indeks, aldri over råfila).

### Fase 3 – Forberedelse til modellering ✓

Binær target (DDoS=1), X/y-splitt (target ALDRI i X), 80/20 stratifisert splitt med fast frø. Skalering utsatt: gjøres per modell senere (RF trenger den ikke).

### Fase 4 – Baseline-modell ✓

Random Forest med standardinnstillinger, fast frø. Trening + prediksjon + sannsynligheter.

### Fase 5 – Evaluering ✓

Confusion matrix, precision/recall/F1 per klasse (recall på DDoS viktigst), ROC-AUC (på sannsynligheter, IKKE harde prediksjoner), feature importance. Resultat: nær perfekt – verifisert at det IKKE er lekkasje eller snarvei; oppgaven er genuint lett på denne fila.

### Fase 6 – Forbedring og generalisering (pågår)

1. Test modellen mot **mandags benign-trafikk** (`monday_benign.csv`) – måler falsk alarm-rate på normaltrafikk fra en annen dag. Viktigste generaliseringstest.
2. Valgfritt: test mot **onsdags DoS** (`wednesday_dos.csv`) – generaliserer den til beslektede angrep?
3. Nye filer MÅ gjennom identisk rensing/preprosessering som treningsdataene.
4. Senere: hyperparameter-tuning (GPU/WSL2-miljøet er klart, se `GPU_SETUP.md` i repoet), eksperiment uten `DestinationPort`, lagre modell for gjenbruk.

## Tekniske notater

- **Stier:** kjør scripts fra prosjektroten, eller bruk `Path(__file__).parent`.
- **Skalering:** per modell, kun tilpasset på treningsdata.
- **DestinationPort:** beholdt i baseline; eksperiment senere: tren uten og sammenlign generalisering.
- **Duplikater:** nesten alle fjernede rader var BENIGN; DDoS falt bare 13.
- **ROC-AUC:** må regnes på sannsynligheter (`predict_proba`), ikke på 0/1-prediksjoner.
- **GPU:** WSL2 + RAPIDS er satt opp, men lønner seg først ved tuning/større data. Baseline kjøres på CPU på Windows-siden.
