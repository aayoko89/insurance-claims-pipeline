from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    "owner": "ade-ayoko",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 1, 1),
}

def run_ingestion():
    subprocess.run(["python", "ingestion/generate_claims.py"], check=True)
    subprocess.run(["python", "ingestion/dirty_claims.py"], check=True)
    print("Ingestion complete")

def run_processing():
    subprocess.run(["python", "processing/clean_claims.py"], check=True)
    print("Processing complete")

def run_warehouse():
    subprocess.run(["python", "warehouse/load_warehouse.py"], check=True)
    print("Warehouse load complete")

def run_validation():
    subprocess.run(["python", "warehouse/query_claims.py"], check=True)
    print("Validation complete")

with DAG(
    dag_id="insurance_claims_pipeline",
    default_args=default_args,
    schedule="0 6 * * *",
    catchup=False,
    tags=["insurance", "claims", "p&c"],
    description="Daily P&C claims ETL pipeline"
) as dag:

    t1 = PythonOperator(task_id="ingest_claims", python_callable=run_ingestion)
    t2 = PythonOperator(task_id="process_claims", python_callable=run_processing)
    t3 = PythonOperator(task_id="load_warehouse", python_callable=run_warehouse)
    t4 = PythonOperator(task_id="validate_output", python_callable=run_validation)

    t1 >> t2 >> t3 >> t4