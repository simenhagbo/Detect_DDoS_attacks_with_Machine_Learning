# Gjennomgang: datalekkasje & modellvaliditet — 2026-06-05

## TL;DR / dom

Pipelinen er **ren for klassisk datalekkasje** — det er gjort flere ting helt riktig her
(duplikater fjernet før split, target droppet fra X, ML-CSV-varianten har ingen IP/Flow
ID/tidsstempel å lekke fra). De nær-perfekte tallene er altså *ekte*, men **smale**:
modellen er i praksis en **LOIC-spesifikk detektor**, ikke en generell DDoS-detektor.
Empirisk bevist nedenfor. Viktigste neste steg: dokumentér modellens rekkevidde ærlig, og
hvis målet er generell deteksjon — tren på flere angrepsverktøy (onsdagens DoS), ikke bare
fredagens LOIC.

## Kontekst

Binær klassifisering DDoS (1) vs. BENIGN (0) på CIC-IDS2017, hovedfil `friday_ddos.csv`
(DDoS LOIT, fredag 15:56–16:16). Suksesskriterium per planen: høy recall på DDoS, lav
falsk-alarm-rate, **evaluert på data den ikke har sett**. Det siste leddet er nøkkelen —
og det er der den nåværende evalueringen kommer til kort: train og test er to tilfeldige
halvdeler av *samme* 20-minutters angrepsvindu.

## Styrker (behold disse)

- **Duplikater fjernet før split.** `drop_duplicates()` skjer i renseskriptet, før fila
  lagres og splittes. Verifisert direkte: **0 av 44 617 testrader** har en identisk
  feature-vektor i treningssettet. Ingen memorering scoret som generalisering.
- **Ingen label-kollisjoner.** 0 distinkte feature-vektorer bærer både BENIGN og DDoS.
  Etiketten er konsistent med dataene.
- **Target lekker ikke inn i X.** `df.drop(columns=['Label','target'])` — riktig.
- **Datavalg uten åpenbare identifikator-lekkasjer.** ML-CSV-varianten mangler IP,
  Flow ID, kildeport og tidsstempel. I et fast oppsett (angriper-IP = angrep) ville disse
  vært perfekt lekkasje; her finnes de ikke. Godt utgangspunkt valgt.
- **Ingen enkeltfeature er en snarvei.** Høyeste univariate AUC er 0.80
  (`BwdPacketLengthMin`). Ingen feature avslører fasiten alene.
- **Riktige metrikk-instinkter i planen.** Recall på DDoS vektlagt; ROC-AUC på
  sannsynligheter, ikke harde prediksjoner. Skalering korrekt utsatt (RF trenger den ikke).

## Funn

### [HØY] Nær-perfekt score måler memorering av ett angrepsverktøy, ikke deteksjonsevne
- **Hva:** Train og test er tilfeldige halvdeler av samme LOIC-angrep + samme ettermiddags
  benign. Scoren (FN=1, FP=0) er korrekt for *denne* fordelingen, men sier lite om ekte
  deteksjon.
- **Bevis (novel-positive-probe):** Modellen trent på fredag, scoret på onsdagens DoS-angrep
  som den aldri har sett:
  | Angrep (onsdag) | n | fanget som angrep |
  |---|---|---|
  | DoS Hulk | 230 124 | **0.07 %** |
  | DoS GoldenEye | 10 293 | **0.00 %** |
  | DoS slowloris | 5 796 | **0.00 %** |
  | DoS Slowhttptest | 5 499 | **0.00 %** |

  Den fanger i praksis **null** av beslektede angrep. Modellen har lært LOIC-fingeravtrykket,
  ikke «angrep generelt».
- **Hvorfor det betyr noe:** Suksesskriteriet er deteksjon på *usett* data. En recall på
  ~1.00 på fredag og ~0.00 på onsdag betyr at de nær-perfekte tallene overselger modellen
  kraftig. Dette er det viktigste funnet i hele gjennomgangen — og det er **ikke** lekkasje,
  men en evalueringsgrense.
- **Retning:** Enten (a) ram inn modellen ærlig som «LOIC/volumetrisk-DDoS-detektor,
  validert kun på det», eller (b) hvis målet er generell deteksjon: tren på flere
  angrepstyper (legg onsdagens DoS inn i treningen) og mål recall på et *utholdt* verktøy.

### [MEDIUM] Renseskriptet dropper konstante kolonner *datadrevet* → kolonnedrift i fase 6
- **Hva:** `[col for col in df.columns if df[col].nunique()==1]` bestemmer hvilke kolonner
  som droppes ut fra *innholdet i akkurat denne fila*. En annen fil (mandag/onsdag) kan ha
  et annet sett konstante kolonner.
- **Bevis:** Tilfeldig gikk det bra her (mandag og onsdag hadde alle 67 trenings-features),
  men det er flaks, ikke garanti. Mekanismen kan stille gi train/score-mismatch.
- **Hvorfor det betyr noe:** Fase 6 forutsetter at nye filer går «gjennom identisk rensing».
  Identisk *kode* gir ikke identiske *kolonner* når kolonnevalget avhenger av dataene.
- **Retning:** Lagre den eksakte trenings-feature-lista (og senere encoders/scalere) og
  `reindex` hver ny fil mot den, i stedet for å re-utlede struktur per fil.

### [MEDIUM] `model.py` er ufullstendig — evalueringen i fase 5 finnes ikke i koden
- **Hva:** Skriptet beregner `y_pred` og `y_probs` (linje 37–40) men skriver aldri ut
  confusion matrix, classification report, ROC-AUC eller feature importance. Planen
  rapporterer alle disse som «gjort».
- **Bevis:** [model.py](../Source/model.py) stopper på `y_probs`. Tallene i PLAN.md kan
  ikke reproduseres fra det som ligger i repoet.
- **Hvorfor det betyr noe:** Resultatet er ikke reproduserbart fra committed kode; en
  fersk kjøring gir bare treningstid, ingen evaluering.
- **Retning:** Legg evalueringsblokken inn i skriptet (eller et eget `evaluate.py`) slik at
  én kjøring produserer alle tallene planen påstår.

### [LAV] Robusthet: hardkodede stier, hardkodet kolonnedropp, ubrukt import
- **Hva / bevis:**
  - Relative stier (`Data/Cleaned_data/...`) krever at scriptet kjøres fra prosjektroten.
  - `df.drop(['FwdHeaderLength.1'], axis=1)` i [data_cleaning.py](../Source/Data_handling/data_cleaning.py)
    mangler `errors='ignore'` → krasjer på en fil uten den kolonnen.
  - `import numpy as np` i model.py er ubrukt.
- **Hvorfor det betyr noe:** Skjørt på tvers av maskiner og inndatafiler; lett å fikse.
- **Retning:** `Path(__file__).parent` for stier; `errors='ignore'` på drop; fjern ubrukt
  import.

### [LAV] Ingen baseline, én enkelt split, ingen lagret modell
- **Hva:** Ingen sammenligning mot triviell baseline (majoritetsklasse gir ~57 %); ett
  punktestimat uten kryssvalidering; modellen lagres ikke (`joblib`) og må trenes på nytt
  hver gang.
- **Hvorfor det betyr noe:** Mindre robust evaluering og ingen gjenbrukbar modell. På et
  saturert problem som dette er CV mest «god skikk», men billig forsikring.
- **Retning:** Legg til en majoritets-baseline i rapporten; vurder k-fold på det utvidede
  (fler-angreps) datasettet; lagre modellen med `joblib`.

## DestinationPort — avklart, ikke et problem
Mistanken i planen om at port kunne være en snarvei er testet og **avkreftet** som
kritisk: DDoS er ~100 % port 80, men å fjerne `DestinationPort` flyttet bare FN fra 1 → 4
(fortsatt FP=0). Den er rank 12 i importance. Flow-formen bærer signalet uansett — som er
nettopp grunnen til at modellen generaliserer dårlig til *andre* verktøy (funn 1).

## Åpne spørsmål
- Generaliserer en modell trent på **fredag + onsdag** til et *fjerde, utholdt* DoS-verktøy?
  (Tren på Hulk+GoldenEye+slowloris+LOIC, hold Slowhttptest utenfor, mål recall.)
- Hvor stabil er 0.07 %-falsk-alarm-raten på mandag over flere frø / med CV?

## Anbefalte neste steg (minst-verdifullt-først)
1. **Fullfør `model.py`s evaluering** (confusion matrix, per-klasse P/R/F1, ROC-AUC på
   `predict_proba`, feature importance) så fase 5-tallene blir reproduserbare.
2. **Skriv inn rekkevidden** i PLAN.md: modellen er per nå LOIC-spesifikk (0 % recall på
   onsdagens DoS). Dette er det ærlige bildet.
3. **Bygg fler-angreps-treningssett** (fredag DDoS + onsdag DoS) og mål recall på et utholdt
   verktøy — den eneste reelle generaliseringstesten.
4. **Persistér feature-schema** (trenings-kolonnelista) og reindekser nye filer mot den, før
   fase 6-kjøringer.

---
*Empiriske prober i denne rapporten ble kjørt read-only mot dataene; ingen prosjektkode ble
endret. Reproduserbar med sklearn 1.7.1 / pandas 2.2.3, `random_state=1`.*
