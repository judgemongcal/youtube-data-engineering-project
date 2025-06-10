import boto3
import time

glue = boto3.client('glue')

ETL_JOB_NAME = 'youtube-stat-parquet-analytics-version'

WAIT_INTERVAL = 30

def start_etl_job(job_name):
    try:
        response = glue.start_job_run(JobName=job_name)
        job_run_id = response['JobRunId']
        print(f"Started ETL job: {job_name} with run ID: {job_run_id}")
        return job_run_id
    except Exception as e:
        raise Exception(f"Failed to start ETL job {job_name}: {str(e)}")

def wait_for_etl_job(job_name, job_run_id):
    while True:
        response = glue.get_job_run(JobName=job_name, RunId=job_run_id)
        state = response['JobRun']['JobRunState']
        print(f"ETL Job {job_name} is in state: {state}")
        
        if state == 'SUCCEEDED':
            print(f"ETL Job {job_name} completed successfully.")
            return
        elif state in ['FAILED', 'TIMEOUT', 'STOPPED']:
            raise Exception(f"ETL Job {job_name} failed with state: {state}")
        else:
            time.sleep(WAIT_INTERVAL)


def lambda_handler(event, context):
    
    job_run_id = start_etl_job(ETL_JOB_NAME)

    wait_for_etl_job(ETL_JOB_NAME, job_run_id)


    return {
        'statusCode': 200,
        'body': 'ETL job and crawler completed successfully.'
    }       