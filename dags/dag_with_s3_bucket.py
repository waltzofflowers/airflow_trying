from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
#import pandas as pd
import csv
from tempfile import NamedTemporaryFile

#holder = datetime(2024, 10, 25)

def fetch_data_from_mssql(**kwargs):
    hook = MsSqlHook(mssql_conn_id='mssql_connection')  # Connection ID defined in Airflow
    sql_query = """
    WITH CTE AS (
        SELECT *, YEAR(date_added) AS year1, MONTH(date_added) AS month1 FROM netflix_titles
    )
    SELECT year1, month1, COUNT(*) FROM CTE
    WHERE year1 IS NOT NULL AND month1 IS NOT NULL
    GROUP BY year1, month1
    ORDER BY year1 DESC, month1 DESC;
    """

    timestamp = datetime.now()

    timestamp_last = timestamp.strftime("%Y%m%d")

    csv_file_path = f'dags/netflix.{timestamp_last}.csv'

    connection = hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()

    with NamedTemporaryFile('w', newline='', delete=False) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['year', 'month', 'count'])
        for row in result:
            writer.writerow(row)


    # with open(csv_file_path, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['year', 'month', 'count'])
    #     for row in result:
    #         writer.writerow(row)

        cursor.close()
        connection.close()

        s3_hook = S3Hook(aws_conn_id='minio_conn')
        s3_hook.load_file(
            filename = f'dags/netflix.{timestamp_last}.csv',
            key = f'netflix.{timestamp_last}.csv',
            bucket_name = 'netflix.year.month.movieadded',
            replace = True
        )

default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id="dag_with_s3_bucket_v1.10", 
    default_args=default_args,
    start_date=datetime(2024, 10, 25),
    #schedule_interval='@daily',  # Since its not a daily task dont include that for the sake of computing power :)
    catchup=False
) as dag:

    fetch_data = PythonOperator(
        task_id="fetch_data",
        python_callable=fetch_data_from_mssql,
        #provide_context=True,  # Ensure that the context is provided
        #do_xcom_push=True  # Ensure that the result is pushed to XCom
    )

    # upload_to_s3 = PythonOperator(
    #     task_id="upload_to_s3",
    #     python_callable=upload_to_s3,
    #     provide_context=True,  # Ensure that the context is provided
    # )

    fetch_data #>> upload_to_s3
