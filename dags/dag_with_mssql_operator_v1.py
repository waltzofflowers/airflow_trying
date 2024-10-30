from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from datetime import datetime

# Function to connect to MSSQL and fetch data
def fetch_data_from_mssql():
    hook = MsSqlHook(mssql_conn_id='mssql_connection')  # Connection ID defined in Airflow
    sql_query = "SELECT TOP 10 * FROM Flight_Data"  # Modify this query as needed
    connection = hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    for row in result:
        print(row)

# Define the DAG
with DAG(
    dag_id='mssql_data_extraction_v1',
    start_date=datetime(2024, 10, 24),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Define the task to fetch data
    fetch_data_task = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data_from_mssql
    )

    fetch_data_task
