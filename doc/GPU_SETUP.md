# GPU-oppsett – WSL2 + RAPIDS (NVIDIA RTX 4060)

> Mål: kjøre ML-modeller (inkl. GPU Random Forest via cuML, GPU-pandas via cuDF og GPU XGBoost) raskest mulig på maskinen.
> Maskinvare: NVIDIA GeForce RTX 4060 laptop (compute capability 8.9 – godt innenfor kravet på ≥ 7.0).
> Kilde: https://docs.rapids.ai/install/

## Viktige forutsetninger (sjekk disse først)

- **Windows 11.** RAPIDS via WSL2 støttes KUN på Windows 11, ikke Windows 10. Sjekk versjonen din før du begynner.
- **NVIDIA-driver:** nyeste Windows-driver for RTX 4060 (CUDA 12 krever driver ≥ 525.60.13 – en oppdatert gaming/studio-driver er langt nyere enn dette).
- **Kun én GPU** støttes (du har én – greit).
- Anbefalt ~2:1 system-RAM mot GPU-RAM (din 8 GB VRAM → 16 GB+ RAM er fint).

## Steg 1 – Installer WSL2 + Ubuntu

- Installer WSL2 med Ubuntu-distribusjonen via Microsofts offisielle metode (`wsl --install` i PowerShell som administrator).
- Bekreft at det er **WSL2**, ikke WSL1 (WSL1 støttes ikke).

## Steg 2 – NVIDIA-driver på Windows-verten

- Installer/oppdater NVIDIA-driveren på **Windows**, ikke inne i WSL2.
- VIKTIG: ikke installer en separat GPU-driver inne i WSL2-instansen. WSL2 bruker Windows-driveren via en passthrough. Å installere driver inni Linux ødelegger oppsettet.

## Steg 3 – Installer Miniforge (conda) inne i WSL2

- Logg inn i Ubuntu/WSL2-instansen.
- Bruk **Miniforge**, ikke Anaconda eller Miniconda. Grunn: RAPIDS bygges mot `conda-forge`-kanalen og er IKKE kompatibel med `defaults`-kanalen som følger med Anaconda/Miniconda. Miniforge unngår dette problemet helt.
- Installer via det offisielle install-scriptet og aktiver `conda-init`.

## Steg 4 – Opprett RAPIDS-miljøet

- Gå til RAPIDS **Release Selector**: https://docs.rapids.ai/install/ og velg: Method = Conda, WSL2, nyeste release, riktig Python- og CUDA-versjon. Selectoren gir deg den NØYAKTIGE kommandoen med riktige versjonspinninger – bruk den, ikke gjett på versjoner.
- Et representativt eksempel på hvordan kommandoen ser ut (bekreft mot selectoren):

  ```
  conda create -n rapids -c rapidsai -c conda-forge -c nvidia \
      cuml cudf python=3.12 'cuda-version>=12.0,<=12.8'
  ```

- Du kan legge til `xgboost` i samme miljø for GPU-akselerert gradient boosting senere.

## Steg 5 – Verifiser installasjonen

- Aktiver miljøet (`conda activate rapids`) og kjør en rask test om cuDF ser GPU-en:

  ```
  python -c "import cudf; print(cudf.Series([1,2,3]))"
  ```

- Hvis dette kjører uten feil, ser RAPIDS GPU-en din.

## Steg 6 – Arbeidsflyt: hvor filene skal ligge

Dette er det viktigste fart-poenget i hele oppsettet:

- Legg prosjektfilene og datasettet **inne i WSL2 sitt Linux-filsystem** (f.eks. under `~/projects/ddos/`), IKKE under `/mnt/c/...` eller OneDrive.
- Grunn: I/O mot `/mnt/c` (Windows-disken) fra WSL2 er tregt. Å lese store CSV-er derfra spiser opp mye av tidsgevinsten fra GPU-en.
- Rediger filene med **VS Code + WSL-utvidelsen** – da jobber du i Linux-miljøet men beholder VS Code-grensesnittet du er vant til.
- Konsekvens: dette betyr at GPU-arbeidet skjer på en kopi i WSL2, adskilt fra OneDrive-mappa. Vurder en bevisst rutine for å synkronisere ferdige resultater tilbake hvis du vil ha dem i OneDrive.

## Bonus – kjør eksisterende sklearn-kode på GPU uten omskriving

- RAPIDS har `cuml.accel` (zero-code-change): den fanger opp scikit-learn-modeller og kjører dem på GPU der det er mulig, ellers faller den tilbake til CPU.
- Det betyr at baseline-scriptet ditt med `RandomForestClassifier` kan kjøres på GPU uten å endre koden – f.eks. ved å kjøre scriptet gjennom `cuml.accel`-laget.
- Dette er grunnen til at WSL2 + RAPIDS er et godt valg: du beholder sklearn-arbeidsflyten din og får GPU-fart oppå.

## Sjekkliste

- [ ] Bekreftet Windows 11
- [ ] Nyeste NVIDIA Windows-driver installert
- [ ] WSL2 + Ubuntu installert
- [ ] Miniforge installert inne i WSL2
- [ ] RAPIDS-miljø opprettet via Release Selector
- [ ] Verifisert med cuDF-test
- [ ] Prosjektfiler flyttet inn i WSL2 Linux-filsystem
- [ ] VS Code + WSL-utvidelse satt opp
