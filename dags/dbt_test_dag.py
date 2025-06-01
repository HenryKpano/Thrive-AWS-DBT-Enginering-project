"""
Airflow DAG to run `dbt test` using DockerOperator.
This DAG validates your data models using dbt's testing framework, ensuring data quality.
"""

import os
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import timedelta
from docker.types import Mount
import pendulum

local_tz = pendulum.timezone("America/Toronto")
# --------------------------------------------------
# CONFIGURATION SECTION
# --------------------------------------------------

DBT_IMAGE = "dbt-redshift-thrive_new"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email': ['henrykpano@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# --------------------------------------------------
# DAG DEFINITION
# --------------------------------------------------

with DAG(
    dag_id='scheduled_dbt_test',
    default_args=default_args,
    description='Run dbt test every day at 6 AM',
    schedule_interval='0 19 * * *',
    start_date=pendulum.datetime(2025, 5, 24, tz=local_tz),
    catchup=False,
    tags=['dbt', 'test', 'quality'],
) as dag:
    
    dbt_test = DockerOperator(
        task_id='run_dbt_test',
        image=DBT_IMAGE,
        api_version='auto',
        auto_remove=True,
        command='dbt test --profiles-dir /usr/app',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        working_dir='/usr/app',
        mount_tmp_dir=False,
        mounts=[
            Mount(
                source='/Users/henk/Documents/DataProjects/Projects/dbt-thrive-eng/dbt_thrive1_redshift_dw',
                target='/usr/app',
                type='bind'
            ),
        ],
        environment={
            'REDSHIFT_DB': os.environ.get('REDSHIFT_DB'),
            'REDSHIFT_USER': os.environ.get('REDSHIFT_USER'),
            'REDSHIFT_SCHEMA': os.environ.get('REDSHIFT_SCHEMA'),
            'REDSHIFT_PORT': os.environ.get('REDSHIFT_PORT'),
            'REDSHIFT_PASSWORD': os.environ.get('REDSHIFT_PASSWORD'),
            'REDSHIFT_HOST': os.environ.get('REDSHIFT_HOST'),
            'DBT_PROFILES_DIR': '/usr/app',
            'DBT_PROJECT_DIR': '/usr/app',
            'DBT_TARGET': 'dev'
        },
    )

    dbt_test
