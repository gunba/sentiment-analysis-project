# Sentiment Analysis Pipeline

This project is an educational demonstration of building a sentiment analysis pipeline using Apache Airflow, Apache Spark, and PostgreSQL, all running within a Docker environment. The pipeline reads a dataset of Amazon product reviews, performs sentiment analysis using TextBlob, and stores the results in a PostgreSQL database.

Please note that this project is primarily intended for educational purposes and may not be suitable for production use.

## Project Overview

The sentiment analysis pipeline consists of the following components:

- Apache Airflow: A platform to programmatically author, schedule, and monitor workflows.
- Apache Spark: A fast and general-purpose cluster computing system for big data processing.
- PostgreSQL: An open-source relational database management system.
- Docker: A platform for developing, shipping, and running applications using containers.

The pipeline performs the following steps:

1. Reads the Amazon product reviews dataset from a TSV file using Apache Spark.
2. Performs sentiment analysis on the review text using the TextBlob library.
3. Calculates the sentiment score and label (positive or negative) for each review.
4. Stores the sentiment analysis results in a PostgreSQL database.

## Prerequisites

To run this project, you need to have the following software installed on your machine:

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

git clone https://github.com/your-username/sentiment-analysis-pipeline.git

2. Navigate to the project directory:

cd sentiment-analysis-pipeline

3. Place the Amazon product reviews dataset file (`amazon_reviews_us_Digital_Software_v1_00.tsv`) in the `data` directory.

4. Start the Docker containers:
docker-compose up -d

5. Access the Airflow web UI in your browser at `http://localhost:8080`.

6. Trigger the `sentiment_analysis_pipeline` DAG to run the sentiment analysis.

7. Once the DAG has completed successfully, you can connect to the PostgreSQL database to view the sentiment analysis results:

docker-compose exec postgres psql -U airflow -d airflow

Run SQL queries to explore the `sentiment_results` table:
```sql
SELECT * FROM sentiment_results LIMIT 10;```

8. To stop and remove the Docker containers, run:

docker-compose down

sentiment-analysis-pipeline/
├── dags/
│   └── sentiment_analysis_dag.py
├── data/
│   └── amazon_reviews_us_Digital_Software_v1_00.tsv
├── plugins/
├── postgres-db-volume/
├── docker-compose.yml
└── README.md

License
This project is licensed under the MIT License.