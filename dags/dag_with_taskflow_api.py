from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    "owner": "airflow",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    dag_id = "dag_with_taskflow_api_v1",
    default_args = default_args,
    start_date = datetime(2024, 10, 21),
    schedule_interval = "@daily"
)
def dag_with_taskflow_api():
    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name' : 'Jerry',
            'last_name' : 'Fridman'
        }

    @task()
    def get_age():
        return 19

    @task()
    def greet(first_name, last_name, age):
        print(f"Hello, I'm {first_name} {last_name} and I'm {age} years old")

    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], last_name=name_dict['last_name'], age=age)

greet_dag = dag_with_taskflow_api()