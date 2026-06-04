# Mutual Fund Analytics Data Dictionary

## Project Overview

This project uses a star schema data warehouse to analyze mutual fund performance, investor transactions, NAV history, and AUM metrics.

---

# Table: dim_fund

**Purpose:** Stores descriptive information about each mutual fund scheme.

| Column Name | Data Type | Definition | Source |
|------------|-----------|------------|---------|
| amfi_code | INTEGER | Unique identifier assigned to each mutual fund scheme by AMFI | nav_history_clean.csv |
| scheme_name | TEXT | Name of the mutual fund scheme | nav_history_clean.csv |
| fund_house | TEXT | Asset Management Company (AMC) managing the scheme | nav_history_clean.csv |
| category | TEXT | Fund category (Equity, Debt, Hybrid, etc.) | nav_history_clean.csv |
| plan | TEXT | Plan type (Direct/Growth/Regular) | nav_history_clean.csv |

**Primary Key:** amfi_code

---

# Table: dim_date

**Purpose:** Stores unique dates used throughout the warehouse.

| Column Name | Data Type | Definition | Source |
|------------|-----------|------------|---------|
| date_key | DATE | Calendar date used for reporting and analysis | NAV & Transaction datasets |

**Primary Key:** date_key

---

# Table: fact_nav

**Purpose:** Stores historical Net Asset Value (NAV) information.

| Column Name | Data Type | Definition | Source |
|------------|-----------|------------|---------|
| amfi_code | INTEGER | Mutual fund identifier | nav_history_clean.csv |
| date_key | DATE | NAV observation date | nav_history_clean.csv |
| nav | REAL | Net Asset Value of the fund on a given date | nav_history_clean.csv |

**Primary Key:** (amfi_code, date_key)

**Foreign Keys:**
- amfi_code → dim_fund.amfi_code
- date_key → dim_date.date_key

---

# Table: fact_transactions

**Purpose:** Stores investor transaction activity.

| Column Name | Data Type | Definition | Source |
|------------|-----------|------------|---------|
| transaction_id | INTEGER | System-generated transaction identifier | ETL Generated |
| investor_id | TEXT | Unique investor identifier | processed_investor_transactions.csv |
| transaction_date | DATE | Date of transaction | processed_investor_transactions.csv |
| amfi_code | INTEGER | Mutual fund identifier | processed_investor_transactions.csv |
| transaction_type | TEXT | Type of transaction (Purchase, Redemption, SIP, etc.) | processed_investor_transactions.csv |
| amount_inr | REAL | Transaction amount in Indian Rupees | processed_investor_transactions.csv |
| state | TEXT | Investor's state | processed_investor_transactions.csv |
| city | TEXT | Investor's city | processed_investor_transactions.csv |
| city_tier | TEXT | Classification of city (Tier 1, Tier 2, Tier 3) | processed_investor_transactions.csv |
| age_group | TEXT | Investor age segment | processed_investor_transactions.csv |
| gender | TEXT | Investor gender | processed_investor_transactions.csv |
| annual_income_lakh | REAL | Annual income in lakhs of INR | processed_investor_transactions.csv |
| payment_mode | TEXT | Payment method used | processed_investor_transactions.csv |
| kyc_status | TEXT | KYC verification status | processed_investor_transactions.csv |

**Primary Key:** transaction_id

**Foreign Keys:**
- amfi_code → dim_fund.amfi_code
- transaction_date → dim_date.date_key

---

# Table: fact_performance

**Purpose:** Stores fund performance and risk metrics.

| Column Name | Data Type | Definition | Source |
|------------|-----------|------------|---------|
| amfi_code | INTEGER | Mutual fund identifier | processed_scheme_performance.csv |
| return_1yr_pct | REAL | Annual return over the last 1 year (%) | processed_scheme_performance.csv |
| return_3yr_pct | REAL | Annualized return over the last 3 years (%) | processed_scheme_performance.csv |
| return_5yr_pct | REAL | Annualized return over the last 5 years (%) | processed_scheme_performance.csv |
| benchmark_3yr_pct | REAL | Benchmark return over 3 years (%) | processed_scheme_performance.csv |
| alpha | REAL | Excess return generated relative to benchmark | processed_scheme_performance.csv |
| beta | REAL | Sensitivity of fund returns to market movements | processed_scheme_performance.csv |
| sharpe_ratio | REAL | Risk-adjusted return metric | processed_scheme_performance.csv |
| sortino_ratio | REAL | Downside risk-adjusted return metric | processed_scheme_performance.csv |
| std_dev_ann_pct | REAL | Annualized standard deviation (%) | processed_scheme_performance.csv |
| max_drawdown_pct | REAL | Maximum observed loss from peak (%) | processed_scheme_performance.csv |
| expense_ratio_pct | REAL | Annual management fee charged (%) | processed_scheme_performance.csv |
| morningstar_rating | INTEGER | Morningstar fund rating | processed_scheme_performance.csv |
| risk_grade | TEXT | Risk classification of the fund | processed_scheme_performance.csv |

**Primary Key:** amfi_code

**Foreign Key:**
- amfi_code → dim_fund.amfi_code

---

# Table: fact_aum

**Purpose:** Stores Assets Under Management (AUM) values.

| Column Name | Data Type | Definition | Source |
|------------|-----------|------------|---------|
| amfi_code | INTEGER | Mutual fund identifier | processed_scheme_performance.csv |
| aum_crore | REAL | Assets Under Management in Crores INR | processed_scheme_performance.csv |

**Primary Key:** amfi_code

**Foreign Key:**
- amfi_code → dim_fund.amfi_code

---

# Schema Relationships

dim_fund (1) ──────< fact_nav

dim_fund (1) ──────< fact_transactions

dim_fund (1) ──────< fact_performance

dim_fund (1) ──────< fact_aum

dim_date (1) ──────< fact_nav

dim_date (1) ──────< fact_transactions

---

# Data Sources

1. nav_history_clean.csv
   - Historical NAV data
   - Fund metadata

2. processed_investor_transactions.csv
   - Investor transaction records
   - Demographic information

3. processed_scheme_performance.csv
   - Performance metrics
   - Risk measures
   - AUM statistics
