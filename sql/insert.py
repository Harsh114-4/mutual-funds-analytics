from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "sql" / "bb.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

nav = pd.read_csv(DATA_DIR / "processed" / "nav_history_clean.csv")
transactions = pd.read_csv(
    DATA_DIR / "processed" / "processed_investor_transactions.csv"
)
performance = pd.read_csv(DATA_DIR / "raw" / "07_scheme_performance.csv")

nav["date"] = pd.to_datetime(nav["date"])
transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

dim_fund = performance[
    [
        "amfi_code",
        "scheme_name",
        "fund_house",
        "category",
        "plan"
    ]
].drop_duplicates(
    subset=["amfi_code"]
)

nav_dates = nav[
    ["date"]
].rename(
    columns={"date": "date_key"}
)

txn_dates = transactions[
    ["transaction_date"]
].rename(
    columns={"transaction_date": "date_key"}
)

dim_date = pd.concat(
    [nav_dates, txn_dates]
).drop_duplicates()

fact_nav = nav[
    [
        "amfi_code",
        "date",
        "nav"
    ]
].rename(
    columns={"date": "date_key"}
)

fact_transactions = transactions[
    [
        "investor_id",
        "transaction_date",
        "amfi_code",
        "transaction_type",
        "amount_inr",
        "state",
        "city",
        "city_tier",
        "age_group",
        "gender",
        "annual_income_lakh",
        "payment_mode",
        "kyc_status"
    ]
].copy()

fact_performance = performance[
    [
        "amfi_code",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "expense_ratio_pct",
        "morningstar_rating",
        "risk_grade"
    ]
].drop_duplicates(
    subset=["amfi_code"]
)

fact_aum = performance[
    [
        "amfi_code",
        "aum_crore"
    ]
].drop_duplicates(
    subset=["amfi_code"]
)

dim_fund.to_sql(
    "dim_fund",
    engine,
    if_exists="append",
    index=False
)

dim_date.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False
)

fact_nav.to_sql(
    "fact_nav",
    engine,
    if_exists="append",
    index=False
)

fact_transactions.to_sql(
    "fact_transactions",
    engine,
    if_exists="append",
    index=False
)

fact_performance.to_sql(
    "fact_performance",
    engine,
    if_exists="append",
    index=False
)

fact_aum.to_sql(
    "fact_aum",
    engine,
    if_exists="append",
    index=False
)

print("Data loaded successfully")
print("dim_fund:", len(dim_fund))
print("dim_date:", len(dim_date))
print("fact_nav:", len(fact_nav))
print("fact_transactions:", len(fact_transactions))
print("fact_performance:", len(fact_performance))
print("fact_aum:", len(fact_aum))