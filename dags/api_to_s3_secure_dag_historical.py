from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import Variable
from datetime import datetime, timedelta
import requests
import json
import logging

# Configuration
API_KEY = Variable.get('weather_api_key')  # e7710580dc646de56ba70eff280ccb1a Replace with your API key
LAT = '40.7128'  # Example: Latitude for New York City
LON = '-74.0060'  # Example: Longitude for New York City
BASE_API_URL = 'https://api.openweathermap.org/data/2.5/forecast'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_api_data():
    """Fetch historical data from the API for the past 5 days and return as JSON string."""
    try:
        # Calculate timestamp for 5 days ago
        # historical_timestamp = int((datetime.now() - timedelta(days=5)).timestamp())
        # Build API URL with parameters for historical data
        api_url = f"{BASE_API_URL}?lat={LAT}&lon={LON}&appid={API_KEY}"
        response = requests.get(api_url)
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching API data: {e}")
        raise

def validate_data(**context):
    """Validate the fetched API data."""
    try:
        data = context['task_instance'].xcom_pull(task_ids='fetch_api_data')
        if not data:
            raise ValueError("No data fetched from API")
        logger.info("Data validated successfully")
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise

def upload_to_s3(**context):
    """Upload data to S3 using Airflow S3Hook."""
    try:
        s3_hook = S3Hook(aws_conn_id='aws_s3_connection')  # Retrieve credentials from Airflow Connection
        bucket_name = Variable.get('s3_bucket_name')  # Retrieve bucket name from Airflow Variable
        data_str = context['task_instance'].xcom_pull(task_ids='fetch_api_data')
        folder_path = Variable.get('s3_folder_path', default_var='weather-data')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f'{folder_path}/historical_api_data_{timestamp}.json'
        s3_hook.load_string(
            string_data=data_str,
            key=file_name,
            bucket_name=bucket_name,
            replace=True
        )
        logger.info(f"Uploaded {file_name} to S3 bucket {bucket_name}")
    except Exception as e:
        logger.error(f"Error uploading to S3: {e}")
        raise

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'api_to_s3_secure_historical_dag',
    default_args=default_args,
    description='Secure DAG to fetch historical data from API and upload to S3 using Airflow Connections',
    schedule_interval='0 19 * * *',
    start_date=datetime(2025, 5, 25),
    catchup=False,
    tags=['Open Wheather', 'API', 's3'],
) as dag:
    fetch_task = PythonOperator(
        task_id='fetch_api_data',
        python_callable=fetch_api_data,
    )
    validate_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
        provide_context=True,
    )
    upload_task = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
        provide_context=True,
    )

    fetch_task >> validate_task >> upload_task