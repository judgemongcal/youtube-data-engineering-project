# youtube-data-engineering-project

## Introduction
This project is a YouTube Data Engineering pipeline built on AWS, designed to process and analyze trending video data at scale for the Canada (CA), United Kingdom (GB), and United States (US) regions. The pipeline automates data ingestion, transformation, and storage, enabling efficient querying, analysis, and reporting of YouTube trends.

As an added feature, a Tableau dashboard is included to provide visual insights into the processed data. The dashboard allows users to explore trends in viewer engagement, video performance, and category-level statistics, offering a more interactive way to interpret and communicate findings.

## Architecture
![architecture](https://github.com/user-attachments/assets/c134933d-cc1d-41a7-ac74-1dc942b272ff)

## Technology Used
For this project, the following programming languages and tools where used:
- Python for the ETL scripts and Lambda functions
- SQL for querying the dataset
- AWS S3 for data storage
- AWS Glue for ETL Jobs and Data Catalog creation
- AWS Lambda for Workflow Orchestration (Step Functions)
- AWS Athena for querying the Data Catalog using SQL

There are multiple ways and tools that can be integrated with AWS Athena to provide real-time data for the dashboard creation but to limit the expense in building this personal project, I manually exported the cleansed and analytics-ready dataset from AWS Athena and used [Tableau Public](https://www.tableau.com/products/public/download) to create the dashboard.

## Dataset Used

The Trending Youtube Video Statistics dataset that was used for this project includes several years of data on daily trending Youtube videos from different regions. For the scope of this project, I limited the data to only process records from United Kingdom (GB), Canada (CA), and United States (US). Each region's data is in a separate file, and can be referenced with the category_id.

This dataset serves as the foundation for the ETL pipeline, analysis scripts, and Tableau dashboard visualizations created in this project.

For more information, you can download the same dataset from this link: [**Trending Youtube Video Statistics**](https://www.kaggle.com/datasets/datasnaek/youtube-new)

## Scripts for the project

- **Lambda Step Function**: [Step Function Code](/step-function/youtube-analytics-etl-workflow.json)
- **Lambda Functions**: [Lambda Functions Code](/lambda-functions/)
- **Glue ETL Jobs**: [Glue ETL Jobs Code](/glue-etl-jobs/)

## Brief Walkthrough of the ETL Workflow

![step function](https://github.com/user-attachments/assets/ae4994ae-57f3-4313-bae6-930b2825782c)

**Step 1**: Once you upload the files in the raw bucket, the event triggers the lambda function  [**youtube-stat-raw-lambda-json-to-parquet**](/lambda-functions/youtube-stat-raw-lambda-json-to-parquet.py).
This lambda function converts the json files into parquet so that it can be processed and queried properly inside AWS.

**Step 2**: The step function triggers the lambda function [**trigger-raw-crawlers**](/lambda-functions/trigger-raw-crawlers.py). It triggers two crawlers simultaneously, which creates a data catalog of the raw data and the raw category reference data (both are provided in the dataset).

**Step 3**: The trigger-cleansing step basically triggers the lambda function [**trigger-cleansing**](/lambda-functions/trigger-cleansing.py). It triggers an Glue ETL Job to remove nulls and convert some string columns into bigint data type. After that, it triggers a crawler assigned for the output path location to create a copy of the cleansed version in our data catalog.

**Step 4**: The last step triggers [**youtube-stat-parquet-analytics-version**](/glue-etl-jobs/youtube-stat-parquet-analytics-version.py), which joins the cleansed data and cleansed category reference data to create the analytics-ready dataset. Lastly, it adds the resulting table into the data catalog.

![step function_success](https://github.com/user-attachments/assets/89b3acd1-4c51-469c-8234-acbd1ca35ce9)


## Additional: Dashboard

This dashboard aims to provide creators necessary information to help them decide which types of videos work well from 2010 - 2018 on three different regions.

For the live dashboard, visit the [**Youtube Data Engineering Project - Dashboard**](https://public.tableau.com/views/YoutubeDataEngineeringProject-Dashboard/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link).
![Dashboard](https://github.com/user-attachments/assets/663db535-550e-4a5e-b095-5ff030aa7eae)


## Got Feedback?
**I'd love to hear your thoughts and feedback to further improve my skills! 🙌🏽**

You can connect with me through my [**LinkedIn**](https://www.linkedin.com/in/judgemongcal/)

Huge thanks to [**Darshil Parmar**](https://github.com/darshilparmar) for the project inspiration and guide!
