from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

#Establish a connection to the SQL Server database
server = 'server'  # Replace 'your_server_name' with your SQL Server instance name
database = 'database'  # Replace 'your_database_name' with your database name
username = 'username'  # Replace 'your_username' with your SQL Server username
password = 'password'  # Replace 'your_password' with your SQL Server password
driver = 'ODBC Driver 17 for SQL Server'  # Replace with your SQL Server driver (e.g., 'ODBC+Driver+17+for+SQL+Server')


def test_connection():
    connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
    try:
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            print("Connection successful!")
    except SQLAlchemyError as e:
        print(f"Error connecting: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

with DAG('test_connection_dag_v4', start_date=datetime(2024, 10, 24), schedule_interval='@daily') as dag:
    test_task = PythonOperator(
        task_id='test_connection',
        python_callable=test_connection,
    )

test_task