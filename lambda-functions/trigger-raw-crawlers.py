import boto3
import time
from concurrent.futures import ThreadPoolExecutor

glue = boto3.client('glue')

# The name of the crawlers depends on your implementation; change accordingly
CRAWLER_1 = 'youtube-stat-raw-glue-catalog'
CRAWLER_2 = 'youtube-stat-raw-csv-crawler-01'

WAIT_INTERVAL = 20

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
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(start_crawler, CRAWLER_1)
        executor.submit(start_crawler, CRAWLER_2)

        executor.submit(wait_for_crawler, CRAWLER_1)
        executor.submit(wait_for_crawler, CRAWLER_2)

    return {
        'statusCode': 200,
        'body': 'Both crawlers completed successfully.'
    }
