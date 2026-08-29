import pandas as pd
from pathlib import Path


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "raw" / "orders.csv"

PROCESSED_DIR = BASE_DIR / "data" / "processed"
REJECTED_DIR = BASE_DIR / "data" / "rejected"

VALID_OUTPUT = PROCESSED_DIR / "valid_orders.csv"
REJECTED_OUTPUT = REJECTED_DIR / "rejected_orders.csv"


VALID_STATUSES = {
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
}


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data():

    print("=" * 60)
    print("LOADING RAW DATA")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    print(f"Total records loaded: {len(df):,}")

    return df


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

def validate_data(df):

    print("\n" + "=" * 60)
    print("VALIDATING DATA")
    print("=" * 60)

    df = df.copy()

    # Store all rejection reasons
    df["rejection_reason"] = ""

    # Missing order ID
    mask = df["order_id"].isna()

    df.loc[mask, "rejection_reason"] += "MISSING_ORDER_ID|"

    # Missing customer ID
    mask = df["customer_id"].isna()

    df.loc[mask, "rejection_reason"] += "MISSING_CUSTOMER_ID|"

    # Invalid quantity
    mask = df["quantity"] <= 0

    df.loc[mask, "rejection_reason"] += "INVALID_QUANTITY|"

    # Invalid unit price
    mask = df["unit_price"] < 0

    df.loc[mask, "rejection_reason"] += "INVALID_UNIT_PRICE|"

    # Invalid order status
    mask = ~df["order_status"].isin(VALID_STATUSES)

    df.loc[mask, "rejection_reason"] += "INVALID_ORDER_STATUS|"

    # Invalid order date
    parsed_date = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    mask = parsed_date.isna()

    df.loc[mask, "rejection_reason"] += "INVALID_ORDER_DATE|"

    # Duplicate order IDs
    mask = (
        df["order_id"].notna()
        & df["order_id"].duplicated(keep=False)
    )

    df.loc[mask, "rejection_reason"] += "DUPLICATE_ORDER_ID|"

    # Remove final separator
    df["rejection_reason"] = (
        df["rejection_reason"]
        .str.rstrip("|")
    )

    return df


# --------------------------------------------------
# SPLIT VALID AND REJECTED RECORDS
# --------------------------------------------------

def split_records(df):

    valid_df = df[
        df["rejection_reason"] == ""
    ].copy()

    rejected_df = df[
        df["rejection_reason"] != ""
    ].copy()

    return valid_df, rejected_df

# --------------------------------------------------
# DATA QUALITY SUMMARY
# --------------------------------------------------

def print_data_quality_summary(df):

    print("\n" + "=" * 60)
    print("DATA QUALITY SUMMARY")
    print("=" * 60)

    checks = {
        "MISSING_ORDER_ID": df["order_id"].isna(),

        "MISSING_CUSTOMER_ID": df["customer_id"].isna(),

        "INVALID_QUANTITY": df["quantity"] <= 0,

        "INVALID_UNIT_PRICE": df["unit_price"] < 0,

        "INVALID_ORDER_STATUS":
            ~df["order_status"].isin(VALID_STATUSES),

        "INVALID_ORDER_DATE":
            pd.to_datetime(
                df["order_date"],
                errors="coerce"
            ).isna(),

        "DUPLICATE_ORDER_ID":
            (
                df["order_id"].notna()
                & df["order_id"].duplicated(keep=False)
            )
    }

    for check_name, mask in checks.items():

        print(
            f"{check_name:<30}"
            f"{mask.sum():>10,}"
        )

# --------------------------------------------------
# SAVE OUTPUT
# --------------------------------------------------

def save_output(valid_df, rejected_df):

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    REJECTED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    valid_df.to_csv(
        VALID_OUTPUT,
        index=False
    )

    rejected_df.to_csv(
        REJECTED_OUTPUT,
        index=False
    )

    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)

    print(f"Valid records:    {len(valid_df):,}")
    print(f"Rejected records: {len(rejected_df):,}")

    print("\nOutput files:")

    print(f"Valid:    {VALID_OUTPUT}")

    print(f"Rejected: {REJECTED_OUTPUT}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    df = load_data()

    validated_df = validate_data(df)

    print_data_quality_summary(
        validated_df
    )

    valid_df, rejected_df = split_records(
        validated_df
    )

    save_output(
        valid_df,
        rejected_df
    )


if __name__ == "__main__":

    main()