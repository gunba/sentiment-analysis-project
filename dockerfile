FROM apache/airflow:2.2.3

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-11-jdk \
         ca-certificates-java \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && update-ca-certificates -f

USER airflow

RUN pip install --no-cache-dir pandas pyspark textblob