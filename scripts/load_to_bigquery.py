from pathlib import Path

import pandas as pd
from google.cloud import bigquery


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ID = "fourth-truck-506708-s5"

BASE_DIR = Path(__file__).resolve().parents[1]

VALID_ORDERS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "valid_orders.csv"
)

CLEAN_ORDERS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "clean_orders.csv"
)

STAGING_TABLE = (
    f"{PROJECT_ID}.ecommerce_staging.staging_orders"
)

CLEAN_TABLE = (
    f"{PROJECT_ID}.ecommerce_clean.clean_orders"
)


# --------------------------------------------------
# BIGQUERY CLIENT
# --------------------------------------------------

client = bigquery.Client(
    project=PROJECT_ID
)


# --------------------------------------------------
# LOAD CSV TO BIGQUERY
# --------------------------------------------------

def load_dataframe(
    dataframe,
    table_id
):

    print("\n" + "=" * 60)

    print(
        f"LOADING DATA TO:\n{table_id}"
    )

    print("=" * 60)

    job_config = (
        bigquery.LoadJobConfig(
            write_disposition=
                bigquery.WriteDisposition.WRITE_TRUNCATE
        )
    )

    job = client.load_table_from_dataframe(
        dataframe,
        table_id,
        job_config=job_config
    )

    job.result()

    table = client.get_table(
        table_id
    )

    print(
        f"Rows loaded: {table.num_rows:,}"
    )

    print(
        f"Columns: {len(table.schema)}"
    )


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("=" * 60)

    print(
        "BIGQUERY DATA LOADING PIPELINE"
    )

    print("=" * 60)

    # ----------------------------------------------
    # LOAD VALIDATED DATA TO STAGING
    # ----------------------------------------------

    print(
        "\nReading validated orders..."
    )

    valid_df = pd.read_csv(
        VALID_ORDERS_FILE
    )

    print(
        f"Records read: {len(valid_df):,}"
    )

    load_dataframe(
        valid_df,
        STAGING_TABLE
    )

    # ----------------------------------------------
    # LOAD CLEAN DATA
    # ----------------------------------------------

    print(
        "\nReading clean orders..."
    )

    clean_df = pd.read_csv(
        CLEAN_ORDERS_FILE
    )

    print(
        f"Records read: {len(clean_df):,}"
    )

    load_dataframe(
        clean_df,
        CLEAN_TABLE
    )

    print("\n" + "=" * 60)

    print(
        "BIGQUERY LOAD COMPLETED SUCCESSFULLY"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()