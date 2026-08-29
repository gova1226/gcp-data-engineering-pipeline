# E-Commerce Data Engineering Pipeline

An end-to-end data engineering pipeline built using Apache Airflow, Docker, PostgreSQL, and Google BigQuery.

The pipeline ingests e-commerce order data, performs data validation and transformation through multiple layers, loads the processed data into BigQuery, and creates analytics views for business reporting.

## Architecture

![E-Commerce Data Engineering Pipeline Architecture](screenshots/architecture.png)

                 E-Commerce Source Data
                         │
                         ▼
                Python Data Generation
                         │
                         ▼
                    Apache Airflow
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Data Validation         Data Transformation
             │                       │
             └───────────┬───────────┘
                         ▼
                    BigQuery
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      STAGING          CLEAN           FACT
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                Analytics Views
          ┌────────┬────────┬────────┐
          ▼        ▼        ▼        ▼
       Monthly  Customer  Product  Payment
                         │
                         ▼
                  Data Quality


## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing and validation |
| Apache Airflow 2.10.5 | Workflow orchestration |
| Docker | Containerization |
| Docker Compose | Local multi-container environment |
| PostgreSQL 16 | Airflow metadata database |
| Google BigQuery | Cloud data warehouse |
| SQL | Transformation and analytics |
| Google Cloud | Cloud data platform |

---

## Project Structure

gcp-data-engineering-pipeline/
│
├── .venv/
│
├── airflow/
│
├── dags/
│   └── ecommerce_pipeline.py
│
├── data/
│   └── Source data files
│
├── logs/
│   └── Airflow logs
│
├── plugins/
│
├── screenshots/
│   └── Project screenshots
│
├── scripts/
│   └── Supporting Python scripts
│
├── sql/
│   ├── analytics_monthly_sales.sql
│   ├── analytics_customer.sql
│   ├── analytics_product.sql
│   ├── analytics_payment.sql
│   └── analytics_status.sql
│
├── docker-compose.yaml
│
└── requirements.txt

# Pipeline Overview

The pipeline is orchestrated using Apache Airflow.

**DAG:**

```text
ecommerce_data_pipeline
```

**Schedule:**

```text
@daily
```

The final DAG contains **11 tasks**, and all 11 tasks completed successfully in the final successful run.

---

# Data Pipeline Layers

## 1. Staging Layer

**Dataset:** `ecommerce_staging`

**Table:** `staging_orders`

The staging layer contains the source order data loaded into BigQuery.

Main fields include:

```text
order_id
customer_id
order_date
product_id
quantity
unit_price
discount
payment_method
order_status
country
rejection_reason
```

---

## 2. Clean Layer

**Dataset:** `ecommerce_clean`

**Table:** `clean_orders`

The clean layer contains validated and transformed order data.

Data-quality checks are performed before the data proceeds to the analytics layer.

---

## 3. Analytics Layer

**Dataset:** `ecommerce_analytics`

**Fact table:** `fact_orders`

The final fact table contains:

```text
order_id
customer_id
order_date
product_id
quantity
unit_price
discount
payment_method
order_status
country
gross_amount
net_amount
order_year
order_month
order_month_name
is_completed
is_cancelled
is_returned
```

---

# Data Quality Validation

## Quantity and Price Validation

```text
TOTAL ROWS: 116221
INVALID QUANTITY: 0
INVALID UNIT PRICE: 0
GROSS CALCULATION MISMATCHES: 0
```

**Result: PASS**

## Order Status Flag Validation

```text
TOTAL ROWS: 116221
DELIVERED FLAG ERRORS: 0
CANCELLED FLAG ERRORS: 0
RETURNED FLAG ERRORS: 0
PLACED/SHIPPED FLAG ERRORS: 0
```

**Result: PASS**

## Customer Validation

```text
TOTAL ROWS: 116221
INVALID CUSTOMER IDs: 0
UNIQUE CUSTOMERS: 29377
NON-POSITIVE QUANTITY: 0
```

**Result: PASS**

## Product Validation

```text
TOTAL ROWS: 116221
INVALID PRODUCT IDs: 0
UNIQUE PRODUCTS: 2000
INVALID PRODUCT FORMAT: 0
```

**Result: PASS**

## Payment Validation

```text
TOTAL ROWS: 116221
INVALID PAYMENT METHODS: 0
UNEXPECTED PAYMENT METHODS: 192
UNIQUE PAYMENT METHODS: 6
```

The 192 unexpected records correspond to the `NAN` category present in the source data. These were treated as a data-quality observation rather than an invalid-record failure.

## Country Validation

```text
TOTAL ROWS: 116221
INVALID COUNTRY: 0
UNEXPECTED COUNTRY: 146
UNIQUE COUNTRIES: 7
```

The 146 unexpected records correspond to the `NAN` category present in the source data.

---

# Data Reconciliation

The staging, clean, and fact layers were reconciled.

Final result:

```text
CLEAN
Rows:           116221
Unique Orders:  116221
Quantity:       349278
Net Sales:      164660809.80

FACT
Rows:           116221
Unique Orders:  116221
Quantity:       349278
Net Sales:      164660809.80
```

Analytics views were also reconciled against the fact table:

```text
FACT      -> 116221 orders
STATUS    -> 116221 orders
MONTHLY   -> 116221 orders
PAYMENT   -> 116221 orders
PRODUCT   -> 116221 orders
CUSTOMER  -> 116221 orders
```

All totals matched:

```text
Orders:       116221
Quantity:     349278
Net Sales:    164660809.80
```

**Result: RECONCILIATION PASSED**

---

# Analytics Views

## Monthly Sales

`v_monthly_sales`

Provides:

- Order count
- Total quantity
- Gross sales
- Total discount
- Net sales
- Average order value
- Year and month

## Customer Analytics

`v_customer_analytics`

Provides:

- Customer order count
- Total quantity
- Gross spend
- Total discount
- Total spend
- Average order value
- First order date
- Last order date

## Product Analytics

`v_product_analytics`

Provides:

- Product order count
- Total quantity
- Gross sales
- Total discount
- Net sales
- Average order value
- Revenue per unit

## Payment Analytics

`v_payment_analytics`

Provides:

- Payment method
- Order count
- Total quantity
- Gross sales
- Total discount
- Net sales
- Average order value

## Status Analytics

`v_status_analytics`

Provides:

- Order status
- Order count
- Total quantity
- Gross sales
- Total discount
- Net sales
- Order percentage
- Sales percentage

---

# Key Business Results

| Metric | Value |
|---|---:|
| Total Orders | 116,221 |
| Unique Orders | 116,221 |
| Unique Customers | 29,377 |
| Unique Products | 2,000 |
| Total Quantity | 349,278 |
| Total Net Sales | 164,660,809.80 |

## Sales by Country

| Country | Net Sales |
|---|---:|
| INDIA | 57,650,909.43 |
| UNITED STATES | 40,742,258.43 |
| UNITED KINGDOM | 19,654,589.61 |
| CANADA | 16,728,897.12 |
| GERMANY | 16,691,501.02 |
| AUSTRALIA | 12,991,040.49 |

## Order Status Distribution

| Status | Orders | Order % |
|---|---:|---:|
| DELIVERED | 71,975 | 61.93% |
| SHIPPED | 17,607 | 15.15% |
| CANCELLED | 11,561 | 9.95% |
| PLACED | 9,249 | 7.96% |
| RETURNED | 5,829 | 5.02% |

---

# Running the Project

## 1. Clone the Repository

```bash
git clone <repository-url>
cd gcp-data-engineering-pipeline
```

## 2. Start Docker Services

```bash
docker compose up -d
```

Check the containers:

```bash
docker compose ps
```

Expected services:

```text
postgres
airflow-init
airflow-webserver
airflow-scheduler
```

## 3. Access Airflow

Open:

```text
http://localhost:8080
```

Default credentials used for this project:

```text
Username: admin
Password: admin
```

## 4. Run the DAG

Open the Airflow UI and select:

```text
ecommerce_data_pipeline
```

Trigger the DAG manually when required.

The DAG is configured to run:

```text
@daily
```

---

# Google Cloud Configuration

The project uses the Google Cloud project:

```text
fourth-truck-506708-s5
```

BigQuery datasets:

```text
ecommerce_staging
ecommerce_clean
ecommerce_analytics
```

Google Cloud credentials are mounted into the Airflow containers through the local Google Cloud configuration.

**Do not commit service-account keys or other credentials to GitHub.**

---

# Final Verification

The final pipeline was tested through Airflow and BigQuery.

```text
Airflow DAG              SUCCESS
11 Airflow Tasks         SUCCESS
Staging Layer            SUCCESS
Clean Layer              SUCCESS
Fact Layer               SUCCESS
Data Quality             PASS
Reconciliation           PASS
Monthly Analytics        SUCCESS
Customer Analytics       SUCCESS
Product Analytics        SUCCESS
Payment Analytics        SUCCESS
Status Analytics         SUCCESS
```

---

# Future Improvements

Possible future enhancements:

- Add incremental data loading
- Add BigQuery partitioning and clustering
- Add Cloud Storage as a landing zone
- Add automated data-quality reporting
- Add email or Slack failure notifications
- Add CI/CD using GitHub Actions
- Add Terraform for infrastructure provisioning
- Add a Power BI or Looker Studio dashboard
- Add monitoring and alerting
- Add unit tests for transformation logic

---

# Author

**Govardhanan**

E-Commerce Data Engineering Pipeline

### Core Technologies

```text
Python
Apache Airflow
Docker
PostgreSQL
Google BigQuery
SQL
Google Cloud
```
