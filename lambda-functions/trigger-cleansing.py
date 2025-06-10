import boto3
import time

glue = boto3.client('glue')

# The ETL job and crawler name depends on your implementation; change accordingly
ETL_JOB_NAME = 'youtube-stat-cleansed-csv-to-parquet'
CRAWLER_NAME = 'youtube-stat-raw-cleansed-csv-to-parquet-etl'
WAIT_INTERVAL = 30 # seconds

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

def start_crawler(name):
    try:
        glue.start_crawler(Name=name)
        print(f"Started crawler: {name}")
    except glue.exceptions.CrawlerRunningException:
        print(f"Crawler {name} is already running.")
    except Exception as e:
        raise Exception(f"Failed to start crawler {name}: {str(e)}")

def wait_for_crawler(name):
    while True:
        response = glue.get_crawler(Name=name)
        crawler = response['Crawler']
        state = crawler['State']
        print(f"Crawler {name} is in state: {state}")

        if state == 'READY':
            last_crawl = crawler.get('LastCrawl')
            if not last_crawl:
                raise Exception(f"Crawler {name} has never run or has no LastCrawl data.")

            status = last_crawl.get('Status')
            if status != 'SUCCEEDED':
                error_message = last_crawl.get('ErrorMessage', 'No error message available')
                raise Exception(f"Crawler {name} finished with status: {status}. Error: {error_message}")

            print(f"Crawler {name} completed successfully.")
            break

        elif state in ['RUNNING', 'STOPPING']:
            print(f"Crawler {name} is still in progress... waiting.")
            time.sleep(WAIT_INTERVAL)

        else:
            raise Exception(f"Unexpected state for crawler {name}: {state}")

def lambda_handler(event, context):
    
    job_run_id = start_etl_job(ETL_JOB_NAME)

    wait_for_etl_job(ETL_JOB_NAME, job_run_id)

    start_crawler(CRAWLER_NAME)
    wait_for_crawler(CRAWLER_NAME)

    return {
        'statusCode': 200,
        'body': 'ETL job and crawler completed successfully.'
    }       