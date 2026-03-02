# Financial Data Engineering Pipeline

An ETL pipeline that fetches, parses, and processes financial instrument data from the European Securities and Markets Authority (ESMA) FIRDS (Financial Instruments Reference Data System) API.

## Overview

This pipeline automates the ingestion of MiFID II financial instrument reference data published by ESMA. It downloads a bulk DLTINS (Delta file for financial instruments) report, parses the ISO 20022 XML format, and outputs a structured CSV file enriched with calculated columns.

**Data Source**: ESMA FIRDS Public API
**Input**: ~498 MB ISO 20022 XML (1M+ financial instrument records)
**Output**: Structured 8-column CSV (~52 MB)

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ETL PIPELINE                                 │
│                                                                     │
│  [ESMA API] ──► [Index XML] ──► [DLTINS URL] ──► [ZIP Download]    │
│                                                                     │
│  [ZIP File] ──► [XML Extract] ──► [Parse XML] ──► [DataFrame]      │
│                                                                     │
│  [DataFrame] ──► [Enrich Columns] ──► [CSV Output]                 │
└─────────────────────────────────────────────────────────────────────┘
```

### Steps

| Step | Module | Description |
|------|--------|-------------|
| 1 | `downloader.py` | Downloads `index.xml` from the ESMA FIRDS Solr API |
| 2 | `index_parser.py` | Parses the index to extract the second DLTINS ZIP file URL |
| 3 | `downloader.py` | Downloads the DLTINS ZIP archive (~15 MB) |
| 4 | `extractor.py` | Extracts the XML file from the ZIP archive |
| 5 | `dltins_parser.py` | Parses the ISO 20022 XML into a pandas DataFrame |
| 6 | `enricher.py` | Adds calculated columns (`a_count`, `contains_a`) |
| 7 | `csv_writer.py` | Exports the enriched DataFrame to CSV |

## Output Schema

| Column | Description |
|--------|-------------|
| `FinInstrmGnlAttrbts.Id` | Unique instrument identifier (ISIN) |
| `FinInstrmGnlAttrbts.FullNm` | Full instrument name |
| `FinInstrmGnlAttrbts.ClssfctnTp` | Classification type code (CFI) |
| `FinInstrmGnlAttrbts.CmmdtyDerivInd` | Whether it is a commodity derivative (`true`/`false`) |
| `FinInstrmGnlAttrbts.NtnlCcy` | Notional currency (e.g. `EUR`) |
| `Issr` | Issuer identifier (LEI code) |
| `a_count` | Number of lowercase `'a'` characters in `FullNm` |
| `contains_a` | `YES` if `a_count > 0`, otherwise `NO` |

## Project Structure

```
Financial-Data-Engineering-Pipeline/
├── app/
│   ├── main.py             # Pipeline orchestrator — runs all 7 steps
│   ├── downloader.py       # HTTP file downloader with streaming support
│   ├── index_parser.py     # Extracts DLTINS URL from ESMA index XML
│   ├── extractor.py        # Extracts XML from ZIP archives
│   ├── dltins_parser.py    # Parses DLTINS ISO 20022 XML to DataFrame
│   ├── enricher.py         # Adds calculated enrichment columns
│   ├── csv_writer.py       # Writes DataFrame to CSV
│   └── storage_client.py   # Placeholder for cloud storage integration
├── tests/
│   ├── test_downloader.py
│   ├── test_index_parser.py
│   ├── test_extractor.py
│   ├── test_dltins_parser.py
│   ├── test_enricher.py
│   └── test_csv_writer.py
├── downloads/              # Downloaded index.xml and ZIP files (git-ignored)
├── extracted/              # Extracted XML files (git-ignored)
├── output/                 # Final CSV output (git-ignored)
└── requirement.txt
```

## Prerequisites

- Python 3.8+
- Internet access to reach the ESMA FIRDS public API

## Installation

```bash
git clone https://github.com/your-username/Financial-Data-Engineering-Pipeline.git
cd Financial-Data-Engineering-Pipeline

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirement.txt
```

## Usage

Run the full pipeline end-to-end:

```bash
python -m app.main
```

The pipeline will log progress for each step and write the final output to `output/dltins_output.csv`.

**Expected runtime**: 5–15 minutes depending on network speed and machine performance (the XML file is ~498 MB).

## Running Tests

```bash
pytest tests/
```

> Note: `test_downloader.py`, `test_extractor.py`, and `test_dltins_parser.py` make real network requests or use locally downloaded files. Run the pipeline at least once before running the full test suite.

To run a specific test module:

```bash
pytest tests/test_enricher.py -v
```

## Technologies

| Library | Purpose |
|---------|---------|
| `pandas` | DataFrame operations and CSV export |
| `requests` | Streaming HTTP downloads |
| `lxml` | XML processing support |
| `pytest` | Unit testing |

## Data Source

This pipeline targets the **ESMA FIRDS** public dataset:

- **API**: `https://registers.esma.europa.eu/solr/esma_registers_firds_files/select`
- **Files**: `https://firds.esma.europa.eu/firds/DLTINS_*.zip`
- **Date range used**: January 17–19, 2021

FIRDS data is published under the [ESMA data policy](https://www.esma.europa.eu/about-esma/legal-notice) and is freely available for public use.
