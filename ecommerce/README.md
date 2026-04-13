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
