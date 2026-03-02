# DLTINS → Financial Instrument ETL 

A compact production-style ETL that downloads ESMA DLTINS ZIP files, extracts XML, parses instrument data, enriches it with derived fields (`a_count`, `contains_a`), and exports a validated CSV.

This repository is a short, deployable pipeline intended to demonstrate reliable data ingestion, schema validation, simple enrichment, and reproducible outputs — exactly the sort of work expected in a data engineering internship.

## One-minute demo (no setup)
1. Clone:
   ```bash
   git clone https://github.com/tanjilh136/Financial-Data-Engineering-Pipeline.git
   cd Financial-Data-Engineering-Pipeline

##Install:

python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

##Run demo:

python -m steeleye_assignment.main

##Inspect output:

output/dltins_output.csv (example output included: output/dltins_output_sample.csv)
