from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_ecommerce_pipeline',
    default_args=default_args,
    description='Daily dbt transformation pipeline for e-commerce analytics',
    schedule_interval='0 6 * * *',  # Run daily at 6 AM
    catchup=False,
    tags=['dbt', 'analytics'],
) as dag:

    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command='cd /opt/airflow/dbt && dbt seed --profiles-dir .',
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt && dbt run --profiles-dir .',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt && dbt test --profiles-dir .',
    )

    # Set dependencies
    dbt_seed >> dbt_run >> dbt_test
