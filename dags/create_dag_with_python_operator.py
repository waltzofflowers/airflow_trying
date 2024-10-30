from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids = 'get_age', key = 'age')
    print(f"Hello {first_name} {last_name}, you are {age} years old")

def get_name(ti):
    ti.xcom_push(key='first_name', value='Jerry')
    ti.xcom_push(key='last_name', value='Fridman')

def get_age(ti):
    ti.xcom_push(key='age', value=19)

with DAG(
    dag_id="create_dag_with_python_operator_v5",
    default_args = default_args,
    description="This is our first python operator that we write",
    start_date= datetime(2024, 10, 20, 17),
    schedule_interval='@daily'
) as dag:

    task1 = PythonOperator(
        task_id = 'greet',
        python_callable = greet,
        #op.kwargs = {'age': 19}
    )

    task2 = PythonOperator(
        task_id = 'get_name',
        python_callable = get_name
    )

    task3 = PythonOperator(
        task_id = 'get_age',
        python_callable = get_age,
    )

    [task2, task3] >> task1