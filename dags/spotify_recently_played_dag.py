from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pendulum

local_tz = pendulum.timezone("US/Central")

default_args = {
    'owner' : 'airflow',
    'retries' : 1,
    'retry_delay' : timedelta(minutes=5)
}

with DAG (
    dag_id = 'spotify_recently_played',
    default_args = default_args,
    description = 'Runs the recently_played_tracks.py script to load Spotify tracks into database',
    schedule_interval = '30 0,12 * * *',
    start_date = datetime(2025, 10, 14, tzinfo=local_tz),
    catchup = False
) as dag:
    
    run_etl = BashOperator(
        task_id = 'run_etl_script',
        bash_command = 'python /opt/airflow/scripts/recently_played_tracks.py'
    )

    run_etl