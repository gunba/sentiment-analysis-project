from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from textblob import TextBlob

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}


def perform_sentiment_analysis():
    spark = SparkSession.builder \
        .appName("SentimentAnalysis") \
        .config("spark.driver.extraClassPath", "/opt/airflow/jars/postgresql-42.7.3.jar") \
        .getOrCreate()
    
    data = spark.read \
        .option("header", "true") \
        .option("delimiter", "\t") \
        .csv("/opt/airflow/data/amazon_reviews_us_Digital_Software_v1_00.tsv")

    def analyze_sentiment(review):
        if review is None:
            return None, None
        else:
            blob = TextBlob(review)
            sentiment_score = blob.sentiment.polarity
            sentiment_label = 'positive' if sentiment_score >= 0 else 'negative'
            return sentiment_score, sentiment_label

    sentiment_udf = spark.udf.register("sentiment_udf", analyze_sentiment, "struct<sentiment_score:float,sentiment_label:string>")

    results = data.select("review_body") \
        .withColumn("sentiment", sentiment_udf("review_body")) \
        .select("review_body", "sentiment.sentiment_score", "sentiment.sentiment_label")
    
    db_url = "jdbc:postgresql://postgres:5432/airflow"
    db_properties = {
        "user": "airflow",
        "password": "airflow",
        "driver": "org.postgresql.Driver"
    }

    results.write \
        .jdbc(url=db_url, table="sentiment_results", mode="append", properties=db_properties)

dag = DAG(
    'sentiment_analysis_pipeline',
    default_args=default_args,
    description='Sentiment Analysis Pipeline',
    schedule_interval=timedelta(days=1),
)

sentiment_analysis_task = PythonOperator(
    task_id='perform_sentiment_analysis',
    python_callable=perform_sentiment_analysis,
    dag=dag,
)

sentiment_analysis_task