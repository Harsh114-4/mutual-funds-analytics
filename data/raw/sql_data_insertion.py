import pandas as pd 
from sqlalchemy import create_engine

df = pd.read_csv(
    "data/processed/01_fund_master.csv"
)
engine = create_engine(
    "sqlite:///bluestock_mf.db"
)
df.to_sql(
    "dim_fund",
    con=engine,
    if_exists="append",
    index=False
)