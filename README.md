# Insurance P&C Claims Data Pipeline

End-to-end data engineering pipeline simulating a Property & Casualty
insurance claims workflow — built to mirror the data platform challenges
at carriers like State Farm.

## What it does

Insurance companies process thousands of claims daily. This pipeline:

- Generates 5000 realistic P&C insurance claims (auto, home, life, renters)
- Simulates real data problems — duplicates, missing values, typos
- Cleans and transforms the dirty data using Python
- Loads clean data into a PostgreSQL star schema data warehouse
- Enables analytics queries by state, claim type, and status

## Tech Stack

| Layer | Tool |
|-------|------|
| Data Generation | Python, Faker |
| Data Cleaning | Pandas |
| Warehouse | PostgreSQL (Redshift-compatible) |
| Orchestration | Apache Airflow (coming soon) |
| CI/CD | GitHub Actions (coming soon) |

## Results

- Processed 5,014 claims end to end
- Caught and removed 186 duplicate records
- Fixed 150 missing claim amounts
- Fixed 100 status typos
- Star schema enables fast analytics by state, type, and status

## How to Run

### Prerequisites
- Python 3.9+
- Docker Desktop

### Setup
git clone https://github.com/aayoko89/insurance-claims-pipeline
cd insurance-claims-pipeline
pip install faker pandas psycopg2-binary sqlalchemy

docker run -d --name claims-warehouse \
  -e POSTGRES_DB=claims_dw \
  -e POSTGRES_USER=engineer \
  -e POSTGRES_PASSWORD=statefarmpipeline \
  -p 5433:5432 postgres:15

### Run the pipeline
python ingestion/generate_claims.py
python ingestion/dirty_claims.py
python processing/clean_claims.py
python warehouse/create_schema.py
python warehouse/load_warehouse.py
python warehouse/query_claims.py

## Project Structure
insurance-claims-pipeline/
├── ingestion/       Generate and dirty the raw data
├── processing/      Clean and transform the data
├── warehouse/       Load and query the database
├── tests/           Automated tests (coming soon)
└── orchestration/   Airflow DAG (coming soon)