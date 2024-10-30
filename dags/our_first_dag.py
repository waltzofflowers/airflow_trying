from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id="our_first_dag_v3",
    default_args = default_args,
    description="This is our first DAG that we write",
    start_date= datetime(2024, 10, 20, 17),
    schedule_interval='@daily'
) as dag:

    task1 = BashOperator(
        task_id="task1",
        bash_command="echo hello, this is the first task!"
    )
    task2 = BashOperator(
        task_id="task2",
        bash_command="echo hello, this is the second task runs after task1!"
    )

    task3 = BashOperator(
        task_id="task3",
        bash_command="echo hello, this is the third task runs after task1!"
    )

    #Task dependency method 1
    # task1.set_downstream(task2)
    # task1.set_downstream(task3)

    #Task dependency method 2
    # task1 >> task2
    # task1 >> task3

    #Task dependency method 3
    task1 >> [task2, task3]