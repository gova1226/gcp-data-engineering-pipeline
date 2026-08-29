# E-Commerce Data Engineering Pipeline

An end-to-end cloud data engineering pipeline that generates, validates, transforms, and analyzes e-commerce order data using Python, Apache Airflow, Docker, and Google BigQuery.

The project demonstrates a complete data engineering workflow from raw data generation through data quality validation and business-ready analytics.

---

## Architecture

![E-Commerce Data Engineering Pipeline Architecture](screenshots/architecture.png)

### End-to-End Flow

```text
Source Data
    │
    ▼
Python Data Generation
    │
    ▼
Raw CSV
    │
    ▼
Data Validation
    │
    ├──────────────► Rejected Records
    │
    ▼
Data Transformation
    │
    ▼
Clean Data
    │
    ▼
Google BigQuery
    │
    ├── Staging Layer
    │
    ├── Clean Layer
    │
    └── Analytics Layer
            │
            ├── Fact Orders
            ├── Monthly Sales
            ├── Customer Analytics
            ├── Product Analytics
            ├── Payment Analytics
            └── Order Status Analytics
```

---

## Project Highlights

- Built an end-to-end e-commerce data engineering pipeline
- Generated and processed **116,221 orders**
- Implemented automated data validation and transformation using Python
- Orchestrated the workflow using **Apache Airflow**
- Containerized the development environment using **Docker Compose**
- Loaded processed data into **Google BigQuery**
- Implemented Staging, Clean, and Analytics data layers
- Created a centralized `fact_orders` analytical fact table
- Created five business-focused BigQuery analytics views
- Implemented data quality and validation checks
- Performed cross-layer reconciliation between BigQuery tables and analytics views
- Configured the Airflow pipeline for daily execution
- Version-controlled the project using Git and GitHub

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation, transformation, validation, and automation |
| Apache Airflow | Workflow orchestration |
| Docker | Containerized development environment |
| Docker Compose | Multi-container orchestration |
| PostgreSQL | Airflow metadata database |
| Google BigQuery | Cloud data warehouse |
| SQL | Data transformation and analytics |
| PowerShell | Local environment and pipeline management |
| Git | Version control |
| GitHub | Source code hosting and portfolio |

---

## Data Architecture

The project follows a layered data architecture separating ingestion, transformation, validation, and analytics.

```text
Raw Data
   │
   ▼
Staging Layer
   │
   ▼
Clean Layer
   │
   ▼
Fact Table
   │
   ├── Monthly Sales Analytics
   ├── Customer Analytics
   ├── Product Analytics
   ├── Payment Analytics
   └── Order Status Analytics
```

### Data Layers

| Layer | Purpose |
|---|---|
| Raw / Source | Original generated e-commerce order data |
| Staging | Initial ingestion of source data into BigQuery |
| Clean | Validated and transformed order data |
| Analytics | Business-ready Fact table and analytical views |

---

## Data Quality & Validation

Automated validation checks are performed before and after the transformation and loading process.

### Validation Checks

The pipeline validates:

- Customer ID format and validity
- Product ID format and validity
- Positive order quantities
- Valid unit prices
- Payment method values
- Country values
- Order status values
- Gross amount calculations
- Order-status derived flags
- Duplicate order IDs
- Cross-layer record and metric reconciliation

### Validation Results

```text
TOTAL ROWS: 116,221

INVALID CUSTOMER IDs: 0
INVALID PRODUCT IDs: 0
INVALID PAYMENT METHODS: 0
INVALID COUNTRY: 0

NON-POSITIVE QUANTITY: 0
INVALID QUANTITY: 0
INVALID UNIT PRICE: 0

GROSS CALCULATION MISMATCHES: 0

DELIVERED FLAG ERRORS: 0
CANCELLED FLAG ERRORS: 0
RETURNED FLAG ERRORS: 0
PLACED/SHIPPED FLAG ERRORS: 0
```

### Reference Data Findings

The validation process also identified records containing unexpected but structurally valid values:

```text
Unexpected Payment Methods: 192
Unique Payment Methods: 6

Unexpected Country Values: 146
Unique Countries: 7
```

These records were identified through validation rather than silently ignored.

---

## BigQuery Data Model

The BigQuery environment is organized into separate logical datasets.

```text
fourth-truck-506708-s5
│
├── ecommerce_staging
│   └── staging_orders
│
├── ecommerce_clean
│   └── clean_orders
│
└── ecommerce_analytics
    ├── fact_orders
    ├── v_monthly_sales
    ├── v_customer_analytics
    ├── v_product_analytics
    ├── v_payment_analytics
    └── v_status_analytics
```

### Layer Reconciliation

The final validation confirmed that all analytical sources contain consistent totals.

| Source | Orders | Quantity | Net Sales |
|---|---:|---:|---:|
| FACT | 116,221 | 349,278 | 164,660,809.80 |
| STATUS | 116,221 | 349,278 | 164,660,809.80 |
| MONTHLY | 116,221 | 349,278 | 164,660,809.80 |
| PAYMENT | 116,221 | 349,278 | 164,660,809.80 |
| PRODUCT | 116,221 | 349,278 | 164,660,809.80 |
| CUSTOMER | 116,221 | 349,278 | 164,660,809.80 |

This confirms that the analytics views reconcile correctly with the central Fact table.

---

## Analytics Layer

The Analytics layer provides business-ready BigQuery views for reporting and downstream analysis.

### Monthly Sales Analytics

`v_monthly_sales`

Provides monthly performance metrics including:

- Order count
- Total quantity
- Gross sales
- Total discount
- Net sales
- Average order value

### Customer Analytics

`v_customer_analytics`

Provides customer-level metrics including:

- Order count
- Total quantity
- Gross spend
- Total discount
- Total spend
- Average order value
- First order date
- Last order date

### Product Analytics

`v_product_analytics`

Provides product-level performance metrics including:

- Order count
- Total quantity
- Gross sales
- Total discount
- Net sales
- Average order value
- Revenue per unit

### Payment Analytics

`v_payment_analytics`

Provides payment-method performance including:

- Order count
- Total quantity
- Gross sales
- Total discount
- Net sales
- Average order value

### Order Status Analytics

`v_status_analytics`

Provides order-status distribution including:

- Order count
- Total quantity
- Gross sales
- Total discount
- Net sales
- Order percentage
- Sales percentage

---

## Key Business Results

The processed dataset contains:

```text
Total Orders        : 116,221
Unique Orders       : 116,221
Unique Customers    : 29,377
Unique Products     : 2,000
Total Quantity      : 349,278
Total Net Sales     : 164,660,809.80
```

### Order Status Distribution

| Order Status | Orders | Order % | Net Sales | Sales % |
|---|---:|---:|---:|---:|
| DELIVERED | 71,975 | 61.93% | 101,907,707.80 | 61.89% |
| SHIPPED | 17,607 | 15.15% | 24,911,575.76 | 15.13% |
| CANCELLED | 11,561 | 9.95% | 16,425,002.13 | 9.98% |
| PLACED | 9,249 | 7.96% | 13,126,198.81 | 7.97% |
| RETURNED | 5,829 | 5.02% | 8,290,325.30 | 5.03% |

### Payment Method Performance

| Payment Method | Orders | Net Sales |
|---|---:|---:|
| PAYPAL | 23,230 | 33,342,535.26 |
| CREDIT_CARD | 23,341 | 32,895,304.01 |
| DEBIT_CARD | 23,243 | 32,871,988.74 |
| BANK_TRANSFER | 23,198 | 32,777,347.31 |
| UPI | 23,017 | 32,514,480.96 |
| NAN | 192 | 259,153.52 |

---

## Top Products by Net Sales

The following products generated the highest net sales in the processed dataset:

| Product ID | Orders | Quantity | Net Sales |
|---|---:|---:|---:|
| PROD_01866 | 81 | 256 | 128,800.36 |
| PROD_01987 | 79 | 241 | 128,600.57 |
| PROD_01442 | 74 | 237 | 127,393.43 |
| PROD_01075 | 75 | 244 | 125,955.39 |
| PROD_01571 | 68 | 250 | 125,742.28 |
| PROD_01159 | 79 | 238 | 125,656.35 |
| PROD_00278 | 76 | 249 | 125,533.43 |
| PROD_01052 | 81 | 233 | 124,828.74 |
| PROD_01731 | 71 | 222 | 123,679.18 |
| PROD_00579 | 75 | 236 | 122,053.22 |

---

## Top Customers by Total Spend

| Customer ID | Orders | Quantity | Total Spend |
|---|---:|---:|---:|
| CUST_023117 | 14 | 49 | 26,458.83 |
| CUST_009214 | 10 | 42 | 26,367.72 |
| CUST_018064 | 11 | 39 | 25,630.82 |
| CUST_009515 | 11 | 41 | 24,991.69 |
| CUST_026930 | 11 | 38 | 24,344.37 |
| CUST_019221 | 10 | 32 | 23,610.10 |
| CUST_013231 | 11 | 36 | 23,139.70 |
| CUST_027735 | 11 | 41 | 23,109.51 |
| CUST_010724 | 11 | 35 | 22,873.60 |
| CUST_028163 | 10 | 36 | 22,715.29 |

---

## Airflow Pipeline

The complete workflow is orchestrated using Apache Airflow.

### DAG

```text
ecommerce_data_pipeline
```

### Pipeline Tasks

The DAG contains 11 tasks covering the complete data engineering workflow:

1. Generate source data
2. Validate raw data
3. Transform and clean data
4. Load data into BigQuery
5. Update the Fact table
6. Run data-quality checks
7. Create monthly sales analytics
8. Create customer analytics
9. Create product analytics
10. Create payment analytics
11. Create order-status analytics

### Scheduling

```text
Schedule: @daily
```

The pipeline has been successfully executed through Airflow, with all 11 tasks completing successfully.

---

## Pipeline Validation Summary

The final pipeline execution was successfully validated through Airflow and BigQuery.

```text
Airflow Tasks              : 11 / 11 SUCCESS
Total Orders               : 116,221
Unique Orders              : 116,221
Total Quantity             : 349,278
Total Net Sales            : 164,660,809.80
Customer Count             : 29,377
Product Count              : 2,000

Gross Calculation Errors   : 0
Quantity Validation Errors : 0
Customer ID Errors         : 0
Product ID Errors          : 0
Status Flag Errors         : 0
```

The final successful Airflow run completed without task failures.

---

## Project Structure

```text
gcp-data-engineering-pipeline/
│
├── dags/
│   └── ecommerce_pipeline.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── rejected/
│
├── scripts/
│   ├── generate_data.py
│   ├── load_to_bigquery.py
│   ├── transform_data.py
│   └── validate_data.py
│
├── sql/
│   ├── analytics_customer.sql
│   ├── analytics_monthly_sales.sql
│   ├── analytics_payment.sql
│   ├── analytics_product.sql
│   ├── analytics_status.sql
│   ├── data_quality.sql
│   └── update_fact_table.sql
│
├── screenshots/
│   └── architecture.png
│
├── docker-compose.yaml
├── requirements.txt
├── README.md
└── .gitignore
```

---

## How to Run

### Prerequisites

Install or configure:

- Docker Desktop
- Git
- Google Cloud account
- Google Cloud project
- BigQuery API
- Appropriate Google Cloud authentication

### Clone the Repository

```bash
git clone https://github.com/gova1226/gcp-data-engineering-pipeline.git
cd gcp-data-engineering-pipeline
```

### Start the Airflow Environment

```bash
docker compose up -d
```

### Check Running Containers

```bash
docker compose ps
```

### Access Airflow

Open:

```text
http://localhost:8080
```

Log in using the credentials configured for the local Docker environment.

### Run the Pipeline

From the Airflow UI:

1. Locate `ecommerce_data_pipeline`
2. Enable the DAG if required
3. Trigger the DAG
4. Monitor task execution
5. Verify all tasks complete successfully

### Stop the Environment

```bash
docker compose down
```

---

## Google Cloud Configuration

The project uses Google BigQuery as the cloud data warehouse.

The pipeline creates and uses the following datasets:

```text
ecommerce_staging
ecommerce_clean
ecommerce_analytics
```

Google Cloud authentication should be configured securely through the local development environment.

**Do not commit service-account private keys, API keys, tokens, or other credentials to GitHub.**

---

## Local Airflow Login

For the local Docker development environment, the configured Airflow credentials can be used to access the web interface.

```text
Username: admin
Password: admin
```

These credentials are intended for local development only and should not be used in a production environment.

---

## Git & Version Control

The project is maintained using Git and hosted on GitHub.

The repository tracks:

- Airflow DAGs
- Python processing scripts
- SQL analytics scripts
- Docker configuration
- Requirements
- README documentation
- Architecture diagram

Generated CSV datasets are intentionally excluded from version control through `.gitignore`.

This keeps the repository lightweight while allowing the pipeline to regenerate the data when required.

---

## Future Improvements

Potential future enhancements include:

- Add incremental data loading instead of full-refresh processing
- Add BigQuery partitioning and clustering
- Add automated unit tests for transformation logic
- Add Airflow failure notifications
- Add CI/CD using GitHub Actions
- Add a Looker Studio or Power BI dashboard
- Add pipeline monitoring and execution metrics
- Add schema validation for incoming source files
- Add infrastructure-as-code using Terraform
- Add automated documentation and data lineage

---

## Project Status

**Status: Completed**

The project demonstrates an end-to-end cloud data engineering workflow:

```text
Data Generation
      ↓
Data Validation
      ↓
Data Transformation
      ↓
BigQuery Ingestion
      ↓
Data Quality Checks
      ↓
Fact Table
      ↓
Business Analytics
      ↓
Airflow Orchestration
```

The final pipeline has been successfully executed and validated using automated data-quality checks, Airflow task execution, and BigQuery cross-layer reconciliation.

---

## Author

**Govardhanan G**

GitHub:  
https://github.com/gova1226
