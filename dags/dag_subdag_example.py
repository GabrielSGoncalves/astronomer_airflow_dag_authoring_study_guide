from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task, dag
from airflow.operators.subdag import SubDagOperator


@task.python
def process_a(partner_name, partner_path):
    print(partner_name)
    print(partner_path)


    