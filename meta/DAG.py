from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from datagouvfr_data_pipelines.meta.task_functions import monitor_dags, notification_mattermost

DAG_NAME = "meta_dag"
date_airflow = "{{ ds }}"

default_args = {
    'email': [
        'pierlou.ramade@data.gouv.fr',
        'geoffrey.aldebert@data.gouv.fr'
    ],
    'email_on_failure': False,
}


with DAG(
    dag_id=DAG_NAME,
    schedule_interval="0 12 * * *",
    start_date=days_ago(1),
    dagrun_timeout=timedelta(minutes=240),
    tags=["monitoring"],
    default_args=default_args,
) as dag:
    monitor_dags = PythonOperator(
        task_id="monitor_dags",
        python_callable=monitor_dags,
    )
    notification_mattermost = PythonOperator(
        task_id="notification_mattermost",
        python_callable=notification_mattermost,
    )

    notification_mattermost.set_upstream(monitor_dags)
