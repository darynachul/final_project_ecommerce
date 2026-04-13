Overview
========

Welcome to Astronomer! This project was generated after you ran 'astro dev init' using the Astronomer CLI. This readme describes the contents of the project, as well as how to run Apache Airflow on your local machine.

Project Contents
================

Your Astro project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs. By default, this directory includes one example DAG:
    - `example_astronauts`: This DAG shows a simple ETL pipeline example that queries the list of astronauts currently in space from the Open Notify API and prints a statement for each astronaut. The DAG uses the TaskFlow API to define tasks in Python, and dynamic task mapping to dynamically print a statement for each astronaut. For more on how this DAG works, see our [Getting started tutorial](https://www.astronomer.io/docs/learn/get-started-with-airflow).
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

Deploy Your Project Locally
===========================

Start Airflow on your local machine by running 'astro dev start'.

This command will spin up five Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- DAG Processor: The Airflow component responsible for parsing DAGs
- API Server: The Airflow component responsible for serving the Airflow UI and API
- Triggerer: The Airflow component responsible for triggering deferred tasks

When all five containers are ready the command will open the browser to the Airflow UI at http://localhost:8080/. You should also be able to access your Postgres Database at 'localhost:5432/postgres' with username 'postgres' and password 'postgres'.

Note: If you already have either of the above ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

Deploy Your Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://www.astronomer.io/docs/astro/deploy-code/

Contact
=======

The Astronomer CLI is maintained with love by the Astronomer team. To report a bug or suggest a change, reach out to our support.



E-commerce Analytics Pipeline
================

Project objective
================
This project creates ELT (Extract, Load, Transform) pipeline for an e-commerce platform. The main goal is to automate the collection of raw data from multiple sources, clean data and transform it for analytical data marts for business decision-making.

Tools
================

Orchestration: Apache Airflow for creating task  and scheduling.
Data Transformation: dbt 
Data Storage: DuckDB 
Containerization: Docker 
Data Sources: MySQL for transactional records and JSON for web event data.

DAG tasks
================

ETL:
-run_etl: the main function that launches ETL
-extract_from_mysql: connects to the MySQL database to get data about  customers, products, orders, order items, and payments.
-extract_json: reads web event data from a JSON file.
-transform: cleans the extracted data
-load_to_duckdb: loads the cleaned data into the DuckDB
DAG :
-run_etl_task: starts the data extraction and loading process.
-should_run_daily: runs the daily data mart models only at 16:00, skipping them at any other time.


Data Architecture 
================

Staging layer
Raw data is loaded in the dbt project where cleaning occurs:
-Column names are standardized across all tables.
-For all data types is choose the correct formats

Mart layer
There are contain KPIs and trends made through SQL queries and window functions.

Business Insights
-mart_most_profitable_payment_method: profitability analysis of different payment methods. Shows which method brings in the highest percentage of revenue
-mart_order_avg_check: analysis of the average check (for each customer and for the store as a whole)
-mart_city_country_revenue: number of customers, orders, and total revenue by city and country
-mart_browser_popularity: the most popular browser among users
-mart_product_category_ranks: rank products in categories by revenue
-mart_order_status: order analysis: quantity and financial share of each status (completed, canceled)

Star schema
================

We used a star schema:
-dimension tables: dim_customers, dim_dates, dim_events_methods, dim_payment_methods, dim_product_categories and dim_products contain descriptive attributes.
-fact tables: fct_order_items contains quantitative metrics regarding sales.

Data Quality and Testing
================

-unique tests 
-notnull tests 
-relationship tests
