"""
Generate synthetic e-commerce order data for the GCP Data Engineering Pipeline.

The dataset intentionally includes controlled data-quality issues so that
the validation layer can identify and route invalid records to a rejected zone.
"""

from pathlib import Path
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


SEED = 42
BASE_RECORDS = 120_000

random.seed(SEED)
np.random.seed(SEED)

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
OUTPUT_FILE = OUTPUT_DIR / "orders.csv"

STATUSES = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]
PAYMENT_METHODS = ["CREDIT_CARD", "DEBIT_CARD", "UPI", "PAYPAL", "BANK_TRANSFER"]
COUNTRIES = ["India", "United States", "United Kingdom", "Canada", "Australia", "Germany"]
PRODUCT_IDS = [f"PROD_{i:05d}" for i in range(1, 2_001)]
CUSTOMER_IDS = [f"CUST_{i:06d}" for i in range(1, 30_001)]


def random_dates(n, start_date, end_date):
    """Return n random dates between start_date and end_date."""
    days = (end_date - start_date).days
    offsets = np.random.randint(0, days + 1, size=n)
    return [
        (start_date + timedelta(days=int(offset))).strftime("%Y-%m-%d")
        for offset in offsets
    ]


def generate_orders(n=BASE_RECORDS):
    """Generate the base valid order population."""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)

    quantity = np.random.randint(1, 6, size=n)
    unit_price = np.round(np.random.uniform(5, 1_000, size=n), 2)
    discount = np.round(
        np.minimum(
            np.random.choice(
                [0, 0, 0, 0, 0.05, 0.10, 0.15, 0.20],
                size=n
            ),
            0.20
        ) * quantity * unit_price,
        2
    )

    return pd.DataFrame(
        {
            "order_id": [f"ORD_{i:07d}" for i in range(1, n + 1)],
            "customer_id": np.random.choice(CUSTOMER_IDS, size=n),
            "order_date": random_dates(n, start_date, end_date),
            "product_id": np.random.choice(PRODUCT_IDS, size=n),
            "quantity": quantity,
            "unit_price": unit_price,
            "discount": discount,
            "payment_method": np.random.choice(PAYMENT_METHODS, size=n),
            "order_status": np.random.choice(
                STATUSES,
                size=n,
                p=[0.08, 0.15, 0.62, 0.10, 0.05]
            ),
            "country": np.random.choice(
                COUNTRIES,
                size=n,
                p=[0.35, 0.25, 0.12, 0.10, 0.08, 0.10]
            ),
        }
    )


def inject_quality_issues(df):
    """
    Inject controlled data-quality issues.

    Returns:
        modified DataFrame
        dictionary containing issue counts
    """
    df = df.copy()
    counts = {}

    # Missing order IDs
    idx = np.random.choice(df.index, size=500, replace=False)
    df.loc[idx, "order_id"] = None
    counts["missing_order_id"] = len(idx)

    # Missing customer IDs
    available = df.index.difference(idx)
    idx = np.random.choice(available, size=400, replace=False)
    df.loc[idx, "customer_id"] = None
    counts["missing_customer_id"] = len(idx)

    # Invalid quantities
    idx = np.random.choice(df.index, size=300, replace=False)
    df.loc[idx[:150], "quantity"] = 0
    df.loc[idx[150:], "quantity"] = -np.random.randint(1, 5, size=150)
    counts["invalid_quantity"] = len(idx)

    # Invalid unit prices
    idx = np.random.choice(df.index, size=200, replace=False)
    df.loc[idx, "unit_price"] = -np.round(
        np.random.uniform(1, 500, size=len(idx)), 2
    )
    counts["invalid_unit_price"] = len(idx)

    # Invalid statuses
    idx = np.random.choice(df.index, size=250, replace=False)
    df.loc[idx, "order_status"] = np.random.choice(
        ["PROCESSING", "PENDING_APPROVAL", "UNKNOWN"],
        size=len(idx)
    )
    counts["invalid_order_status"] = len(idx)

    # Invalid dates
    idx = np.random.choice(df.index, size=150, replace=False)
    df.loc[idx, "order_date"] = np.random.choice(
        ["2025-13-40", "invalid_date", "2024-02-30"],
        size=len(idx)
    )
    counts["invalid_order_date"] = len(idx)

    # Missing payment method
    idx = np.random.choice(df.index, size=200, replace=False)
    df.loc[idx, "payment_method"] = None
    counts["missing_payment_method"] = len(idx)

    # Missing country
    idx = np.random.choice(df.index, size=150, replace=False)
    df.loc[idx, "country"] = None
    counts["missing_country"] = len(idx)

    # Duplicate orders: append copies with existing order IDs.
    duplicate_source = df[
        df["order_id"].notna()
    ].sample(n=2_000, random_state=SEED).copy()
    df = pd.concat([df, duplicate_source], ignore_index=True)
    counts["duplicate_order_rows_added"] = len(duplicate_source)

    return df, counts


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    orders = generate_orders()
    orders, issue_counts = inject_quality_issues(orders)

    # Shuffle to make duplicates/non-valid rows less obvious in the raw source.
    orders = orders.sample(frac=1, random_state=SEED).reset_index(drop=True)
    orders.to_csv(OUTPUT_FILE, index=False)

    print("=" * 65)
    print("E-COMMERCE DATASET GENERATION COMPLETE")
    print("=" * 65)
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Total records: {len(orders):,}")
    print(f"Total columns: {len(orders.columns)}")
    print()
    print("INTENTIONALLY INJECTED DATA-QUALITY ISSUES")
    print("-" * 65)
    for issue, count in issue_counts.items():
        print(f"{issue:35} {count:>10,}")
    print("=" * 65)


if __name__ == "__main__":
    main()
