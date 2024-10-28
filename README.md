# SERVIER : PYTHON & SQL TESTS

This project provides a solution for Servier’s data engineering technical test. The main objective is to analyze journal data to identify drug mentions within PubMed articles and clinical trial studies. The project is structured with multiple Python modules, configuration files, and testing scripts.

# Table of contents :

- [Part 1 - Data Pipeline](#Part-1---data-pipeline)
  - [Project Hypotheses](#Project---Hypotheses)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
  - [Commands](#commands)
  - [production](#production)
    - [A. Deployment](#a-deployment)
    - [B. Orchestration](#b-orchestration)
  - [How to adapt the code for Big Data](#how-to-adapt-the-code-for-big-data)
- [Part 2 - SQL](#Part-2---sql)

# Part 1 - Data Pipeline

## Project Hypotheses

- An intermediate data quality layer is provided during the cleaning process.
- Only cleaned data is analyzed for the final JSON output, with empty entries like missing IDs discarded. Articles without drug mentions are excluded.
Each drug mention is linked to a unique instance.
- Input data is available in both .csv and .json formats.
- Output data includes two JSON files: drug_mentions_graph.json and most_mentioned_journal.json.
- The project supports multiple input files and can process corrupted JSON files if necessary.

## Project Structure

This structure provides an organized environment for data ingestion, cleaning, processing, exporting, and testing, with clear separation between raw data, intermediate preparation, output results, and supporting modules.

```plaintext
.
├── Dockerfile
├── README.md
├── Sql
│   ├── Req1.sql
│   └── Req2.sql
├── conftest.py
├── data
│   ├── Landing
│   │   ├── Src_clinical_trials.csv
│   │   ├── Src_drugs.csv
│   │   ├── Src_pubmed.csv
│   │   └── Src_pubmed.json
│   └── Preparation
│       ├── clinical_trials.csv
│       ├── drugs.csv
│       ├── pubmed.csv
│       └── pubmed.json
├── output
│   ├── ad_hoc
│   │   └── most_mentioned_journal.json
│   └── link_graph
│       └── drug_mentions_graph.json
├── poetry.lock
├── pyproject.toml
├── pytest.ini
├── src
│   ├── __init__.py
│   ├── ad_hoc.py
│   ├── config.py
│   ├── data_export
│   │   ├── __init__.py
│   │   └── export_json.py
│   ├── data_ingestion
│   │   ├── __init__.py
│   │   └── load_data.py
│   ├── data_processing
│   │   ├── __init__.py
│   │   ├── cleaning.py
│   │   └── processing.py
│   └── main.py
└── tests
    ├── __init__.py
    ├── test_ad_hoc.py
    ├── test_cleaning.py
    ├── test_export_json.py
    ├── test_load_data.py
    └── test_processing.py
```
## Installation

To get started, please confirm that the following requirements are met to run the code on your computer :
- `Python >= 3.10.9` -  [official website](https://www.python.org/downloads/).
- `git` to clone the repository or download the repository (.zip)
- `poetry` for packaging (downloaded using `pip install poetry`) 
-  `docker` (downloaded from the [official website](https://www.docker.com/products/docker-desktop/)).

## Commands
 Generate the drug_mentions_graph.json file
```bash
poetry run main 
```
Generate the most_mentioned_journal.json file
```bash
poetry run ad_hoc 
```

Unit Test
```bash
poetry run pytest -vv tests/
 ```

Buile docker Image
```bash
docker build -t servier-test-python-ramlatest -f 
 ```
This setup will execute the code inside the container.
```bash
docker run -it servier-test-python-ram:latest 
```

## production

### A. Deployment
To optimize the production pipeline setup, consider these improvements:

- Use environment-specific variables (.env_dev, .env_ppd, .env_prd) for better testing and environment separation.
- Implement CI/CD with tools like GitLab CI, Jenkins, or Cloud Build to streamline "Development to Production" deployment.
- Choose a CI/CD strategy, such as:
- Create 3-branch model (develop, preprod, prod) with triggers on merge requests.
- Create PRs (Pull Requests)
- Run security, regression, and end-to-end tests in CI/CD with reporting.

### B. Orchestration

Orchestration with Cloud Composer
To manage and schedule the execution of this pipeline in production, Google Cloud Composer (built on Apache Airflow) is used for orchestration.

- Cloud Composer Integration Steps:

1.  Define the DAG (Directed Acyclic Graph) :

   - Create a DAG file in Airflow to define the pipeline tasks.
   - Each task (e.g., data extraction, transformation) is represented as a Python function or script to be called with Airflow operators (PythonOperator, BashOperator).

2.  Environment Setup:

 - In Google Cloud Console, create a Cloud Composer environment with the required resources and configurations (e.g., machine type, disk space).

3. Upload DAG File:

 - Place the DAG file in the Cloud Composer dags/ folder to activate it.

  4. Environment Variables:

   - Set environment variables within the Cloud Composer environment for each pipeline stage (e.g., API_KEY, DB_CONNECTION_STRING).

 5. Trigger and Monitor DAG:

   - Use the Airflow UI to trigger the DAG manually or set up a schedule for periodic execution.

   - Monitor task progress, check logs, and troubleshoot any issues directly from the Airflow UI.

## How to adapt the code for Big Data

To scale the code for Big Data (millions of rows, terabytes of data), there are two options for the ETL pipeline:

1. Use pySpark instead of pandas to enable distributed computation:

 - Adapting the code should be relatively simple due to the syntax similarities between pandas and pySpark.
 - The code should run on a virtual machine with sufficient resources (CPU, GPU, memory) to handle the workload.

2. Alternatively, load the data into BigQuery and perform ETL transformations using SQL:

 - Store input files in Google Cloud Storage for seamless ingestion into BigQuery.
 - Use SQL transformations orchestrated within a version-controlled dbt project to manage and automate the process.
 - Output files should be saved to Google Cloud Storage, with lifecycle policies set up to prevent accidental data loss.


 # Part 2 - SQL 

- Before we start, here is a list of hypothesis that I infered before solving the problems :
    - The tables are inside a dataset called `test_servier`
    - We will be using BigQuery's SQL notation
    - Since we are using BigQuery, then we assume that the date will automatically be fixed and converted to %Y-%m-%d instead of %d/%m/%Y, so no need to use `FORMAT_DATE()` or `PARSE_DATE()` functions

- Query 1 : Daily sales between January 1st 2019 and December 31st 2019 
```sql
SELECT
    date AS date,
    SUM(prod_price * prod_qty) AS ventes
FROM
    `test_sevrier.TRANSACTIONS`
WHERE
    date BETWEEN "2019-01-01" AND "2019-12-31"
GROUP BY
    date
ORDER BY
    date ASC
```


- Query 2 : Decoration and Furniture sales by client, between January 1st 2019 and December 31st 2019 
```sql
SELECT
    t.client_id AS client_id,
    SUM(
        CASE
            WHEN pn.product_type = 'MEUBLE' THEN t.prod_price * t.prod_qty
            ELSE 0
        END
    ) AS ventes_meuble,
    SUM(
        CASE
            WHEN pn.product_type = 'DECO' THEN t.prod_price * t.prod_qty
            ELSE 0
        END
    ) AS ventes_deco
FROM
    `test_sevrier.TRANSACTIONS` AS t
LEFT JOIN `test_sevrier.PRODUCT_NOMENCLATURE` AS pn ON t.prod_id = pn.product_id
WHERE
    t.date BETWEEN "2019-01-01" AND "2019-12-31"
GROUP BY
    client_id
```