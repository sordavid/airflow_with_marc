from airflow import DAG

# imports HttpSensor 
from airflow.providers.http.sensors.http import HttpSensor

from datetime import datetime, timedelta

# standard default_args setup
default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# takes 3 arguments (Dag id, start date and schedule interval)
# catchup=False - you will prevent running non triggered dag run between current date and start date. (basically wont run unused dags)
with DAG("forex_data_pipeline", start_date=datetime(2023, 7, 20), 
    schedule_interval="@daily", default_args=default_args, catchup=False) as dag:

    is_forex_rates_available = HttpSensor(
        task_id="is_forex_rates_available",
        ## forex_api - is the ID of the connection you are going to create
        http_conn_id="forex_api",
        endpoint="marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b",
        # response_check - is for ensure we get a response 
        response_check=lambda response: "rates" in response.text,
        # poke_interval - defines frequency where sensor checks is true or false for 5 seconds 
        poke_interval=5, 
        # timeout - after 20s after sensor is running, we will get a timeout
        timeout=20,
    )