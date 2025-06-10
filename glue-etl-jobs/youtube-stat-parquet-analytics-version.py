import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node youtube_stat
youtube_stat_node1749386640831 = glueContext.create_dynamic_frame.from_catalog(database="db-youtube-stat-cleansed", table_name="youtube_stat", transformation_ctx="youtube_stat_node1749386640831")

# Script generated for node cleansed_stat_ref_data
cleansed_stat_ref_data_node1749386656146 = glueContext.create_dynamic_frame.from_catalog(database="db-youtube-stat-cleansed", table_name="cleansed_stat_ref_data", transformation_ctx="cleansed_stat_ref_data_node1749386656146")

# Script generated for node Join
Join_node1749386717242 = Join.apply(frame1=youtube_stat_node1749386640831, frame2=cleansed_stat_ref_data_node1749386656146, keys1=["category_id"], keys2=["id"], transformation_ctx="Join_node1749386717242")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=Join_node1749386717242, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1749386592744", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1749386813301 = glueContext.getSink(path="s3://youtube-stat-analytics-southeast-1-dev", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=["region", "category_id"], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1749386813301")
AmazonS3_node1749386813301.setCatalogInfo(catalogDatabase="db-youtube-stat-analytics",catalogTableName="final_analytics")
AmazonS3_node1749386813301.setFormat("glueparquet", compression="snappy")
AmazonS3_node1749386813301.writeFrame(Join_node1749386717242)
job.commit()