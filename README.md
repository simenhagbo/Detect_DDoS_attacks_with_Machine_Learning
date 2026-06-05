# DDoS-deteksjon med maskinlæring

Et læringsprosjekt der jeg bygger en maskinlæringsmodell for å oppdage nettverksangrep, trent på CIC-IDS2017-datasettet. Hovedmålet er å lære hvordan ML faktisk brukes mot cybersikkerhet – jeg begynner på cybersikkerhetsstudier høsten 2026, og dette er forberedelse til det. Det jeg lærer på veien betyr mer enn den ferdige modellen. Jeg skriver koden selv, steg for steg, framfor å generere den.

## Hva prosjektet gjør – og hvor langt det er kommet

Kort fortalt: les inn nettverks-flows fra CIC-IDS2017, rens dataene, og tren en klassifikator til å skille angrep fra normal trafikk.

Jeg prøver å være ærlig om status, for det er en del av poenget med å lære:

Den første baselinen – en Random Forest trent på fredagens DDoS-data – traff nesten perfekt, med recall og precision rundt 1.0. Det så bra ut helt til jeg testet modellen på DoS-angrep fra en annen dag, som den aldri hadde sett under trening. Da fanget den så godt som ingenting: under 0,1 % av DoS Hulk, og 0 % av de tre andre verktøyene. Modellen hadde altså ikke lært «angrep» – den hadde lært fingeravtrykket til ett enkelt verktøy (LOIC). De nær-perfekte tallene oversolgte den kraftig.

Det funnet er grunnen til at prosjektet nå handler om **generalisering**: trene på flere angrepstyper og måle ærlig hvor godt modellen takler et angrep den ikke har sett under trening (leave-one-attack-out). Det er den egentlige testen, og den er vanskeligere enn den første scoren ga inntrykk av.

## Datasettet

Prosjektet bruker [CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html) fra Canadian Institute for Cybersecurity. Det er fem dager med simulert nettverkstrafikk – normal aktivitet blandet med et utvalg angrep (DoS, DDoS, brute force, portscan, web-angrep, infiltration og botnet).

**Dataene ligger ikke i dette repoet.** De er på over 1 GB, og datasettet har sine egne bruksvilkår. Du laster dem ned selv fra lenken over (CSV-variantene, «MachineLearningCSV») og legger dem i `Data/CSV_files/`.

Bruker du datasettet skal denne artikkelen siteres:

> Iman Sharafaldin, Arash Habibi Lashkari, Ali A. Ghorbani, "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization", ICISSP 2018.

## Struktur

```
Source/
  Data_handling/
    Inspect_data.py      utforsker rådataene (labels, shapes)
    data_cleaning.py     renser fredags-DDoS-fila (baselinen)
    utvidet_dataset.py   bygger et samlet fler-angreps-datasett (pågår)
  model.py               trener og evaluerer baseline-modellen
Data/                    her legges datasettet (utelatt fra repoet)
```

## Komme i gang

```
pip install pandas numpy scikit-learn
```

1. Last ned CIC-IDS2017 (MachineLearningCSV) og legg CSV-filene i `Data/CSV_files/`.
2. Kjør scriptene fra prosjektroten, f.eks. `python Source/Data_handling/Inspect_data.py`.

## Status

- [x] Utforsking og rensing av dataene
- [x] Baseline Random Forest på fredagens DDoS
- [x] Ærlig evaluering – som avslørte at baselinen er LOIC-spesifikk
- [ ] Fler-angreps-datasett (DoS + DDoS + benign)
- [ ] Leave-one-attack-out-evaluering
- [ ] Senere: anomalideteksjon på egen trafikk

## Lisens

MIT – se [LICENSE](LICENSE).
