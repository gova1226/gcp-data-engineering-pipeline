
from datetime import datetime, timedelta
import subprocess

from airflow import DAG
from airflow.operators.python import PythonOperator

from google.cloud import bigquery

# --------------------------------------------------
# PROJECT PATHS INSIDE THE AIRFLOW CONTAINER
# --------------------------------------------------

DATA_PATH = "/opt/airflow/data"
SCRIPTS_PATH = "/opt/airflow/scripts"
SQL_PATH = "/opt/airflow/sql"

PROJECT_ID = "fourth-truck-506708-s5"


# --------------------------------------------------
# TASK FUNCTIONS
# --------------------------------------------------

def run_data_quality_check():
    """Run data quality checks in BigQuery."""

    client = bigquery.Client(project=PROJECT_ID)

    sql_file = f"{SQL_PATH}/data_quality.sql"

    with open(sql_file, "r") as file:
        query = file.read()

    print("Running data quality checks...")

    results = client.query(query, location="asia-south1").result()

    failed_checks = []

    for row in results:
        check_name = row["check_name"]
        failed_records = row["failed_records"]

        print(
            f"{check_name}: "
            f"{failed_records} failed records"
        )

        if failed_records > 0:
            failed_checks.append(
                f"{check_name}: {failed_records}"
            )

    if failed_checks:
        raise ValueError(
            "Data quality checks failed:\n"
            + "\n".join(failed_checks)
        )

    print("All data quality checks passed.")

def update_fact_table():
    """Create or update the analytics fact table."""

    client = bigquery.Client(project=PROJECT_ID)

    sql_file = f"{SQL_PATH}/update_fact_table.sql"

    with open(sql_file, "r") as file:
        query = file.read()

    print("Updating fact_orders table...")

    job = client.query(query, location="asia-south1")

    job.result()

    print(
        "fact_orders table updated successfully."
    )

def create_analytics_view(sql_filename):
    """Create a single BigQuery analytics view."""

    client = bigquery.Client(project=PROJECT_ID)

    sql_file = f"{SQL_PATH}/{sql_filename}"

    print(f"Running {sql_filename}...")

    with open(sql_file, "r") as file:
        query = file.read()

    job = client.query(query)
    job.result()

    print(f"{sql_filename} completed successfully.")

def check_source_file():
    """Check whether the source orders file exists."""

    import os

    file_path = f"{DATA_PATH}/raw/orders.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )

    print(f"Source file found: {file_path}")


def run_validation():
    """Run the data validation script."""

    result = subprocess.run(
        [
            "python",
            f"{SCRIPTS_PATH}/validate_data.py"
        ],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception("Data validation failed")


def run_transformation():
    """Run the transformation script."""

    result = subprocess.run(
        [
            "python",
            f"{SCRIPTS_PATH}/transform_data.py"
        ],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception("Data transformation failed")


def load_to_bigquery():
    """Load staging and clean data into BigQuery."""

    result = subprocess.run(
        [
            "python",
            f"{SCRIPTS_PATH}/load_to_bigquery.py"
        ],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise Exception("BigQuery loading failed")


# --------------------------------------------------
# DEFAULT DAG SETTINGS
# --------------------------------------------------

default_args = {
    "owner": "govardhanan",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


# --------------------------------------------------
# DAG DEFINITION
# --------------------------------------------------

with DAG(
    dag_id="ecommerce_data_pipeline",
    default_args=default_args,
    description="End-to-end GCP e-commerce data engineering pipeline",
    start_date=datetime(2026, 8, 1),
    schedule="@daily",
    catchup=False,
    tags=["gcp", "bigquery", "data-engineering", "ecommerce"],
) as dag:

    data_quality = PythonOperator(
        task_id="data_quality_check",
        python_callable=run_data_quality_check,
    )

    update_fact = PythonOperator(
        task_id="update_fact_table",
        python_callable=update_fact_table,
    )

    analytics_monthly = PythonOperator(
    task_id="analytics_monthly_sales",
    python_callable=create_analytics_view,
    op_kwargs={
        "sql_filename": "analytics_monthly_sales.sql"
    },
)

    analytics_customer = PythonOperator(
        task_id="analytics_customer",
        python_callable=create_analytics_view,
        op_kwargs={
            "sql_filename": "analytics_customer.sql"
        },
    )

    analytics_product = PythonOperator(
        task_id="analytics_product",
        python_callable=create_analytics_view,
        op_kwargs={
            "sql_filename": "analytics_product.sql"
        },
    )

    analytics_payment = PythonOperator(
        task_id="analytics_payment",
        python_callable=create_analytics_view,
        op_kwargs={
            "sql_filename": "analytics_payment.sql"
        },
    )

    analytics_status = PythonOperator(
        task_id="analytics_status",
        python_callable=create_analytics_view,
        op_kwargs={
            "sql_filename": "analytics_status.sql"
        },
    )

    check_source = PythonOperator(
        task_id="check_source_file",
        python_callable=check_source_file,
    )

    validate = PythonOperator(
        task_id="validate_data",
        python_callable=run_validation,
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=run_transformation,
    )

    load_bigquery = PythonOperator(
        task_id="load_to_bigquery",
        python_callable=load_to_bigquery,
    )

    # --------------------------------------------------
    # TASK DEPENDENCIES
    # --------------------------------------------------

check_source >> validate >> transform >> load_bigquery >> data_quality >> update_fact

update_fact >> analytics_monthly
update_fact >> analytics_customer
update_fact >> analytics_product
update_fact >> analytics_payment
update_fact >> analytics_status