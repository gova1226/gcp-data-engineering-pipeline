import pandas as pd
from pathlib import Path


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "valid_orders.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "clean_orders.csv"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data():

    print("=" * 60)
    print("LOADING VALIDATED DATA")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    print(f"Records loaded: {len(df):,}")

    return df


# --------------------------------------------------
# TRANSFORM DATA
# --------------------------------------------------

def transform_data(df):

    print("\n" + "=" * 60)
    print("TRANSFORMING DATA")
    print("=" * 60)

    df = df.copy()

    # --------------------------------------------------
    # STANDARDIZE TEXT COLUMNS
    # --------------------------------------------------

    text_columns = [
        "customer_id",
        "product_id",
        "payment_method",
        "order_status",
        "country"
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    # --------------------------------------------------
    # CONVERT ORDER DATE
    # --------------------------------------------------

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    # --------------------------------------------------
    # CALCULATE FINANCIAL METRICS
    # --------------------------------------------------

    df["gross_amount"] = (
        df["quantity"]
        * df["unit_price"]
    )

    df["net_amount"] = (
        df["gross_amount"]
        - df["discount"]
    )

    # Round monetary columns

    money_columns = [
        "unit_price",
        "discount",
        "gross_amount",
        "net_amount"
    ]

    df[money_columns] = (
        df[money_columns]
        .round(2)
    )

    # --------------------------------------------------
    # DATE DERIVED COLUMNS
    # --------------------------------------------------

    df["order_year"] = (
        df["order_date"]
        .dt.year
    )

    df["order_month"] = (
        df["order_date"]
        .dt.month
    )

    df["order_month_name"] = (
        df["order_date"]
        .dt.month_name()
    )

    # --------------------------------------------------
    # ORDER STATUS FLAGS
    # --------------------------------------------------

    df["is_completed"] = (
        df["order_status"]
        == "DELIVERED"
    ).astype(int)

    df["is_cancelled"] = (
        df["order_status"]
        == "CANCELLED"
    ).astype(int)

    df["is_returned"] = (
        df["order_status"]
        == "RETURNED"
    ).astype(int)

    print("Transformation completed.")

    return df


# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------

def save_data(df):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n" + "=" * 60)
    print("TRANSFORMATION RESULTS")
    print("=" * 60)

    print(f"Records transformed: {len(df):,}")
    print(f"Output file: {OUTPUT_FILE}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    df = load_data()

    transformed_df = transform_data(df)

    save_data(
        transformed_df
    )


if __name__ == "__main__":

    main()