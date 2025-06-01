from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import Variable
from datetime import datetime, timedelta
import requests
import pandas as pd
import io
import logging

# Configuration
API_KEY = 'e7710580dc646de56ba70eff280ccb1a'  # Store in Airflow Variables for security
LAT = '40.7128'  # Latitude for New York City
LON = '-74.0060'  # Longitude for New York City
BASE_API_URL = 'https://api.openweathermap.org/data/2.5/forecast'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_api_data():
    """Fetch 5-day forecast data from OpenWeatherMap API."""
    try:
        api_url = f"{BASE_API_URL}?lat={LAT}&lon={LON}&appid={API_KEY}"
        response = requests.get(api_url)
        response.raise_for_status()
        logger.info("Successfully fetched API data")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching API data: {e}")
        raise

def validate_data(**context):
    """Validate the fetched API data."""
    try:
        data = context['task_instance'].xcom_pull(task_ids='fetch_api_data')
        if not data or 'list' not in data or not data['list']:
            raise ValueError("No valid forecast data fetched")
        if 'city' not in data or not data['city']:
            raise ValueError("No city data in API response")
        logger.info("Data validated successfully")
        return data
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise

def convert_to_csv(**context):
    """Convert API JSON data to CSV format."""
    try:
        data = context['task_instance'].xcom_pull(task_ids='validate_data')
        if not data or 'list' not in data:
            raise ValueError("No forecast data to convert")
        
        # Flatten the 'list' array into records
        records = []
        city = data.get('city', {})
        for item in data['list']:
            record = {
                'dt': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                'temp': item['main'].get('temp'),
                'feels_like': item['main'].get('feels_like'),
                'temp_min': item['main'].get('temp_min'),
                'temp_max': item['main'].get('temp_max'),
                'pressure': item['main'].get('pressure'),
                'humidity': item['main'].get('humidity'),
                'clouds_all': item['clouds'].get('all'),
                'wind_speed': item['wind'].get('speed'),
                'wind_deg': item['wind'].get('deg'),
                'wind_gust': item['wind'].get('gust', None),
                'visibility': item.get('visibility'),
                'pop': item.get('pop'),
                'weather_id': item['weather'][0].get('id') if item.get('weather') else None,
                'weather_main': item['weather'][0].get('main') if item.get('weather') else None,
                'weather_description': item['weather'][0].get('description') if item.get('weather') else None,
                'dt_txt': item.get('dt_txt'),
                'rain_3h': item['rain']['3h'] if 'rain' in item and '3h' in item['rain'] else None,
                'city_id': city.get('id'),
                'city_name': city.get('name'),
                'city_lat': city.get('coord', {}).get('lat'),
                'city_lon': city.get('coord', {}).get('lon'),
                'city_country': city.get('country'),
                'city_population': city.get('population'),
                'city_timezone': city.get('timezone'),
                'city_sunrise': datetime.fromtimestamp(city.get('sunrise', 0)).strftime('%Y-%m-%d %H:%M:%S') if city.get('sunrise') else None,
                'city_sunset': datetime.fromtimestamp(city.get('sunset', 0)).strftime('%Y-%m-%d %H:%M:%S') if city.get('sunset') else None,
            }
            records.append(record)
        
        # Convert to DataFrame
        df = pd.DataFrame(records)
        # Write to CSV in memory
        output = io.StringIO()
        df.to_csv(output, index=False)
        csv_data = output.getvalue()
        output.close()
        logger.info("Data converted to CSV successfully")
        return csv_data
    except Exception as e:
        logger.error(f"Error converting to CSV: {e}")
        raise

def upload_to_s3(**context):
    """Upload CSV data to S3."""
    try:
        s3_hook = S3Hook(aws_conn_id='aws_s3_connection')
        bucket_name = Variable.get('s3_bucket_name')
        folder_path = Variable.get('s3_folder_path', default_var='weather-data')
        csv_data = context['task_instance'].xcom_pull(task_ids='convert_to_csv')
        if not csv_data:
            logger.warning("No CSV data to upload")
            return
        
        # Use timestamp for unique file name
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f"{folder_path}/forecast_api_data_{timestamp}.csv"
        s3_hook.load_string(
            string_data=csv_data,
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
    'api_to_s3_secure_forecast_dag',
    default_args=default_args,
    description='Secure DAG to fetch 5-day forecast data from OpenWeatherMap API, convert to CSV, and upload to S3',
    schedule_interval='0 19 * * *',
    start_date=datetime(2025, 5, 25),
    catchup=False,
    tags=['Open Weather', 'API', 's3', 'CSV'],
) as dag:
    fetch_task = PythonOperator(
        task_id='fetch_api_data',
        python_callable=fetch_api_data,
        provide_context=True,
    )
    validate_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
        provide_context=True,
    )
    convert_task = PythonOperator(
        task_id='convert_to_csv',
        python_callable=convert_to_csv,
        provide_context=True,
    )
    upload_task = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
        provide_context=True,
    )

    fetch_task >> validate_task >> convert_task >> upload_task