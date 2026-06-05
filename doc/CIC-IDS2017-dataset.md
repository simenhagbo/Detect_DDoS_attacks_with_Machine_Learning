# CIC-IDS2017 – Datasettkontekst

> Kontekstfil for prosjektet "ML-basert DDoS-deteksjon". Inneholder informasjon om datasettet CIC-IDS2017 fra Canadian Institute for Cybersecurity (UNB).
> Kilde: https://www.unb.ca/cic/datasets/ids-2017.html

## Oversikt

CIC-IDS2017 (Intrusion Detection Evaluation Dataset) inneholder benign (normal) trafikk og de mest oppdaterte vanlige angrepene, og ligner ekte trafikk fra den virkelige verden (PCAP-filer). Det inkluderer også resultatene av nettverkstrafikk-analyse gjort med **CICFlowMeter**, med merkede (labeled) flows basert på tidsstempel, kilde- og destinasjons-IP, kilde- og destinasjonsporter, protokoller og angrepstype (CSV-filer).

Bakgrunnstrafikken ble generert med et **B-Profile-system** (Sharafaldin et al., 2016) som profilerer abstrakt atferd av menneskelig interaksjon for å skape naturalistisk benign trafikk. Datasettet er bygget på den abstrakte atferden til 25 brukere basert på protokollene HTTP, HTTPS, FTP, SSH og e-post.

## Innsamlingsperiode

- **Start:** Mandag 3. juli 2017, kl. 09:00
- **Slutt:** Fredag 7. juli 2017, kl. 17:00
- **Totalt:** 5 dager
- Mandag = kun benign trafikk (normal dag). Angrep ble utført både formiddag og ettermiddag tirsdag, onsdag, torsdag og fredag.

### Filer per dag

| Dag | Innhold | Størrelse |
|-----|---------|-----------|
| Mandag | Normal aktivitet | 11.0 GB |
| Tirsdag | Angrep + normal aktivitet | 11 GB |
| Onsdag | Angrep + normal aktivitet | 13 GB |
| Torsdag | Angrep + normal aktivitet | 7.8 GB |
| Fredag | Angrep + normal aktivitet | 8.3 GB |

## Angrep i datasettet

Inkluderer de mest vanlige angrepene basert på McAfee-rapporten fra 2016:

- Brute Force (FTP, SSH)
- DoS
- DDoS
- Web-baserte angrep (Brute Force, XSS, SQL Injection)
- Infiltration
- Heartbleed
- Botnet
- Port Scan

### Tidslinje for angrep

**Mandag 3. juli 2017** – Benign (kun normal menneskelig aktivitet).

**Tirsdag 4. juli 2017 – Brute Force**
- FTP-Patator (09:20 – 10:20)
- SSH-Patator (14:00 – 15:00)
- Angriper: Kali, 205.174.165.73
- Offer: WebServer Ubuntu, 205.174.165.68 (lokal IP: 192.168.10.50)

**Onsdag 5. juli 2017 – DoS / DDoS**
- DoS slowloris (09:47 – 10:10)
- DoS Slowhttptest (10:14 – 10:35)
- DoS Hulk (10:43 – 11:00)
- DoS GoldenEye (11:10 – 11:23)
- Angriper: Kali, 205.174.165.73 | Offer: WebServer Ubuntu, 205.174.165.68 (192.168.10.50)
- Heartbleed Port 444 (15:12 – 15:32)
  - Angriper: Kali, 205.174.165.73 | Offer: Ubuntu12, 205.174.165.66 (192.168.10.51)

**Torsdag 6. juli 2017**
- Formiddag – Web-angrep:
  - Brute Force (09:20 – 10:00)
  - XSS (10:15 – 10:35)
  - SQL Injection (10:40 – 10:42)
  - Angriper: Kali, 205.174.165.73 | Offer: WebServer Ubuntu, 205.174.165.68 (192.168.10.50)
- Ettermiddag – Infiltration:
  - Dropbox-nedlasting / Meta exploit Win Vista (14:19–14:21 og 14:33–14:35) – Offer: Windows Vista, 192.168.10.8
  - Cool disk – MAC (14:53 – 15:00) – Offer: MAC, 192.168.10.25
  - Dropbox-nedlasting Win Vista (15:04 – 15:45) – Offer: Windows Vista, 192.168.10.8
  - Andre steg (Portscan + Nmap): Angriper Vista 192.168.10.8 → alle andre klienter

**Fredag 7. juli 2017**
- Formiddag – Botnet ARES (10:02 – 11:02)
  - Angriper: Kali, 205.174.165.73
  - Ofre: Win 10 (192.168.10.15), Win 7 (192.168.10.9), Win 10 (192.168.10.14), Win 8 (192.168.10.5), Vista (192.168.10.8)
- Ettermiddag – Port Scan (flere firewall-regler på/av mellom 13:55 og 15:29; sS, sT, sF, sX, sN, sP, sV, sU, sO, sA, sW, sR, sL, sI, b)
  - Angriper: Kali, 205.174.165.73 | Offer: Ubuntu16, 205.174.165.68 (192.168.10.50)
- Ettermiddag – **DDoS LOIT (15:56 – 16:16)**
  - Angripere: Tre Win 8.1-maskiner, 205.174.165.69 – 71
  - Offer: Ubuntu16, 205.174.165.68 (192.168.10.50)

> **Relevant for dette prosjektet:** DDoS-trafikk finnes primært i **fredagens ettermiddagsdata (DDoS LOIT, 15:56–16:16)**. DoS-angrepene (onsdag) er relaterte og kan også være nyttige for modellering.

## Nettverkstopologi

**Firewall:** 205.174.165.80, 172.16.0.1
**DNS + DC-server:** 192.168.10.3

### Angripernettverk (outsiders)
- Kali: 205.174.165.73
- Win: 205.174.165.69, .70, .71

### Offernettverk (insiders)
- Web server 16 (public): 192.168.10.50, 205.174.165.68
- Ubuntu server 12 (public): 192.168.10.51, 205.174.165.66
- Ubuntu 14.4 32B: 192.168.10.19
- Ubuntu 14.4 64B: 192.168.10.17
- Ubuntu 16.4 32B: 192.168.10.16
- Ubuntu 16.4 64B: 192.168.10.12
- Win 7 Pro 64B: 192.168.10.9
- Win 8.1 64B: 192.168.10.5
- Win Vista 64B: 192.168.10.8
- Win 10 Pro 32B: 192.168.10.14
- Win 10 64B: 192.168.10.15
- MAC: 192.168.10.25

### NAT-prosess på firewall (typisk)
```
Angrep:  205.174.165.73 -> 205.174.165.80 (firewall) -> 172.16.0.1 -> 192.168.10.50
Svar:    192.168.10.50 -> 172.16.0.1 -> 205.174.165.80 -> 205.174.165.73
```

## Features og filformater

- Mer enn **80 nettverks-flow-features** ekstrahert med CICFlowMeter.
- Datasettet leveres som:
  - **PCAP-filer** (rå pakkedata med full payload)
  - **GeneratedLabelledFlows.zip** – merkede flows
  - **MachineLearningCSV.zip** – CSV-filer beregnet for maskinlæring og dyp læring (anbefalt utgangspunkt for dette prosjektet)
- CICFlowMeter: https://github.com/ISCX/CICFlowMeter | http://netflowmeter.ca/

## De 11 kriteriene for et pålitelig referansedatasett (Gharib et al., 2016)

1. **Complete Network configuration** – modem, firewall, switcher, routere, og variasjon av OS (Windows, Ubuntu, Mac OS X).
2. **Complete Traffic** – brukerprofileringsagent og 12 ulike maskiner i offernettverket med ekte angrep fra angripernettverket.
3. **Labelled Dataset** – benign og angreps-labels for hver dag.
4. **Complete Interaction** – dekker både innen og mellom interne LAN, samt internettkommunikasjon.
5. **Complete Capture** – all trafikk fanget via mirror-port og lagret på lagringsserver.
6. **Available Protocols** – HTTP, HTTPS, FTP, SSH og e-postprotokoller.
7. **Attack Diversity** – web-baserte, brute force, DoS, DDoS, infiltration, Heartbleed, bot og scan.
8. **Heterogeneity** – nettverkstrafikk fra hovedswitch, memory dumps og systemkall under angrep.
9. **Feature Set** – over 80 features via CICFlowMeter, levert som CSV.
10. **MetaData** – tid, angrep, flows og labels forklart i artikkelen.

## Sitering / Lisens

Datasettet (PCAP, profiler, merkede flows og CSV-filer) er offentlig tilgjengelig for forskere. Ved bruk skal følgende artikkel siteres:

> Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani, "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization", 4th International Conference on Information Systems Security and Privacy (ICISSP), Portugal, January 2018.

## Relaterte ressurser

- Webinar: "Enhancing Generalizability in DDoS Attack Detection Systems through Transfer Learning and Ensemble Learning Approaches" (Dr. Mahdi Rabbani) – https://youtu.be/zaRsIJy21xM
- Relatert datasett: BCCC-CIC-IDS2017 (Behaviour-Centric Cybersecurity Center, York University) – https://www.yorku.ca/research/bccc/ucs-technical/cybersecurity-datasets-cds/
