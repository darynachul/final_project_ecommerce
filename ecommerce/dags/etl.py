import os
import duckdb
import pandas as pd
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import Variable


BASE_PATH = Variable.get("base_path", default_var="/usr/local/airflow/include")
DUCKDB_PATH = os.path.join(BASE_PATH, "warehouse.duckdb")
WEB_EVENTS_PATH = os.path.join(BASE_PATH, "web_events.json")


MYSQL_TABLES = ["customers", "products", "orders", "order_items", "payments"]

def extract_from_mysql():
    mysql_hook = MySqlHook(mysql_conn_id='sql_connection')
    dataframes = {}
    
    for table in MYSQL_TABLES:
        print(f"Extraction: fetching data from table '{table}'...")
        df = mysql_hook.get_pandas_df(sql=f"SELECT * FROM {table}")
        dataframes[table] = df
        
    return dataframes

def extract_json(path):
    """Екстракція даних з JSON файлу."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} is not found.")
    
    df = pd.read_json(path)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def transform(dataframes):
    for df_name in dataframes:
        df = dataframes[df_name]

        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()
    return dataframes

def load_to_duckdb(dataframes, events_df, duckdb_path):
    os.makedirs(os.path.dirname(duckdb_path), exist_ok=True)
    con = duckdb.connect(duckdb_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")

  
    for table_name, df in dataframes.items():
        con.execute(f"CREATE OR REPLACE TABLE raw.{table_name} AS SELECT * FROM df")

    con.execute("CREATE OR REPLACE TABLE raw.web_events AS SELECT * FROM events_df")
    con.close()

def run_etl():
    print("--- Start of ETL process ---")
    

    mysql_data = extract_from_mysql()
    events_df  = extract_json(WEB_EVENTS_PATH)
    mysql_data = transform(mysql_data)
    load_to_duckdb(mysql_data, events_df, DUCKDB_PATH)
    print(f"--- Success! Data is loaded into {DUCKDB_PATH} ---")

if __name__ == "__main__":
    run_etl()