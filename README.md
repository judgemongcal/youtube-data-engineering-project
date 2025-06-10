# youtube-data-engineering-project

## Introduction
This project is a YouTube Data Engineering pipeline built on AWS, designed to process and analyze trending video data at scale for the Canada (CA), United Kingdom (GB), and United States (US) regions. The pipeline automates data ingestion, transformation, and storage, enabling efficient querying, analysis, and reporting of YouTube trends.

As an added feature, a Tableau dashboard is included to provide visual insights into the processed data. The dashboard allows users to explore trends in viewer engagement, video performance, and category-level statistics, offering a more interactive way to interpret and communicate findings.

## Architecture

## Technology Used
For this project, the following programming languages and tools where used:
- Python for the ETL scripts and Lambda functions
- SQL for querying the dataset
- AWS S3 for data storage
- AWS Glue for ETL Jobs and Data Catalog creation
- AWS Lambda for Workflow Orchestration (Step Functions)
- AWS Athena for querying the Data Catalog using SQL
- 
## Dataset Used

This project uses the [Trending YouTube Video Statistics](https://www.kaggle.com/datasets/datasnaek/youtube-new) dataset, originally published on Kaggle by DataSnaker. The dataset contains daily records of trending YouTube videos for multiple regions, including metadata such as video titles, channel names, category IDs, publish dates, views, likes, dislikes, comment counts, and more.

For the purpose of this project, only the data from the Canada (CA), United Kingdom (GB), and United State (US) regions were used.



## Scripts for the project
