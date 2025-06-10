import awswrangler as wr
import pandas as pd
import urllib.parse
import os

# Note: If you're going to try out this project on your own, don't forget
# to declare the environment variables under the configuration tab > environment variables
# in AWS Lambda

os_input_s3_cleansed_layer = os.environ['s3_cleansed_layer']
os_input_glue_catalog_db_name = os.environ['glue_catalog_db_name']
os_input_glue_catalog_table_name = os.environ['glue_catalog_table_name']
os_input_write_data_operation = os.environ['write_data_operation']

def lambda_handler(event, context):
    # Get the object from the event and show its contetn type
    if 'Records' in event:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    else:
        bucket = event['bucket']
        key = event['key']
    try:

        # Create DF from content
        df_raw = wr.s3.read_json('s3://{}/{}'.format(bucket, key))

        # Extract the required columns
        df_step_1 = pd.json_normalize(df_raw['items'])

        # Write to S3
        wr_response = wr.s3.to_parquet(
            df = df_step_1,
            path = os_input_s3_cleansed_layer,
            dataset = True,
            database = os_input_glue_catalog_db_name,
            table = os_input_glue_catalog_table_name,
            mode = os_input_write_data_operation
        )

        return wr_response

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
