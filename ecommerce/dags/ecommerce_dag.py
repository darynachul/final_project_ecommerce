import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator


DAGS_PATH = "/usr/local/airflow/dags"
DBT_PROJECT_PATH = "/usr/local/airflow/dbt/ecommerce_transform"

default_args = {
    "owner": "daryna",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def run_etl_task():
    import importlib.util
    path_to_script = os.path.join(DAGS_PATH, "etl.py")
    spec = importlib.util.spec_from_file_location("etl_custom", path_to_script)
    etl_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(etl_module)
    etl_module.run_etl()

def should_run_daily(**context):
    dag_run = context['dag_run']
    
    if dag_run.run_type == 'manual':
        return "dbt_build_daily"
    
    current_hour = context["data_interval_start"].hour
    if current_hour == 16:
        print(f"Scheduled launch at {current_hour} - launching daily build")
        return "dbt_build_daily"
    
    print(f"Scheduled launch at {current_hour} - skipping daily build")
    return "skip_daily"

with DAG(
    dag_id="ecommerce_pipeline_v3", 
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="0 * * * *", 
    catchup=False,
    tags=["ecommerce"],
) as dag:

    etl_task = PythonOperator(
        task_id="extract_and_load",
        python_callable=run_etl_task,
    )

    dbt_hourly = BashOperator(
        task_id="dbt_build_hourly",
        bash_command=f"cd {DBT_PROJECT_PATH} && dbt seed && dbt build --select tag:hourly --profiles-dir .",
    )

    branch_daily = BranchPythonOperator(
        task_id="check_if_daily",
        python_callable=should_run_daily,
    )

    dbt_daily = BashOperator(
        task_id="dbt_build_daily",
        bash_command=f"cd {DBT_PROJECT_PATH} && dbt seed && dbt build --select tag:daily --profiles-dir .",
    )

    skip_daily = EmptyOperator(task_id="skip_daily")


    etl_task >> dbt_hourly >> branch_daily >> [dbt_daily, skip_daily]
