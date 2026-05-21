





























# import requests
# url="http://localhost:8000/docs#/Info/get_transactions_api_bank_transactions_get"
# respoonse=requests.get(url)
# print(respoonse.json())

# Your code will fail because you are sending a request to the Swagger UI HTML page, not to the actual API endpoint.

# This URL:

# "http://localhost:8000/docs#/Info/get_transactions_api_bank_transactions_get"
# is only for viewing API documentation in the browser.

# You should call the real endpoint instead.

# Example:

# import requests

# url = "http://localhost:8000/api/bank/transactions"

# response = requests.get(url)

# print(response.json())
# Why?

# /docs → Swagger UI webpage

# /api/bank/transactions → actual API route returning JSON

# If you still get an error, check:

# Is your FastAPI server running?

# uvicorn main:app --reload
# Open this in browser:

# http://localhost:8000/docs
# Find the exact endpoint path under:

# GET

# POST

# etc.

# Then use that exact path in requests.get().

# Also fix the spelling mistake:

# response
# not

# respoonse

# Creating Polars DataFrame...
# Pipeline failed: unexpected value while building Series of type String; found value of type Float64: 5000.0

# Hint: Try setting strict=False to allow passing data with mixed types.
# (de-project) PS D:\De_project\Bronze> 

# This error happens because one column in your data contains mixed data types.

# Example:

# ["Ram", "Hari", 5000.0]
# Polars tries to create a String column, but suddenly finds a Float64.

# Common causes:

# Empty values becoming NaN

# Numbers mixed with text

# CSV columns having inconsistent types

# You can fix it in several ways.

# Option 1 — Use strict=False (quick fix)
# import polars as pl

# df = pl.DataFrame(data, strict=False)
# or

# pl.Series("col", data, strict=False)
# This allows mixed values and auto-converts them.

# Option 2 — Convert values before creating DataFrame
# Example:

# data["amount"] = [str(x) for x in data["amount"]]
# or

# data["amount"] = [float(x) for x in data["amount"]]
# depending on what the column should actually contain.

# Option 3 — While reading CSV
# If reading CSV:

# df = pl.read_csv(
#     "file.csv",
#     infer_schema_length=10000
# )
# or explicitly define schema:

# df = pl.read_csv(
#     "file.csv",
#     schema={
#         "amount": pl.Float64,
#         "name": pl.String
#     }
# )
# Most likely in your pipeline:

# a column expected as string has numeric values like 5000.0

# or a numeric column has text somewhere

# Print the problematic data before DataFrame creation:

# print(data)
# or inspect dtypes:

# print(df.dtypes)
# to find the inconsistent column.


# Uploading parquet file to S3...
# Pipeline failed: Unable to locate credentials

# This error means your code is trying to upload to Amazon Web Services S3, but AWS credentials are not configured on your computer.

# You need:

# AWS Access Key

# AWS Secret Key

# Option 1 — Configure using AWS CLI (recommended)
# Install AWS CLI:

# AWS CLI Download

# Then run:

# aws configure
# It will ask:

# AWS Access Key ID:
# AWS Secret Access Key:
# Default region:
# Default output format:
# Example:

# AWS Access Key ID: AKIA....
# AWS Secret Access Key: xxxxx
# Default region: us-east-1
# Default output format: json
# Credentials get stored automatically.

# Option 2 — Directly inside Python
# import boto3

# s3 = boto3.client(
#     "s3",
#     aws_access_key_id="YOUR_ACCESS_KEY",
#     aws_secret_access_key="YOUR_SECRET_KEY",
#     region_name="us-east-1"
# )
# Avoid hardcoding credentials in real projects.

# Option 3 — Environment Variables
# Windows PowerShell:

# $env:AWS_ACCESS_KEY_ID="your_key"
# $env:AWS_SECRET_ACCESS_KEY="your_secret"
# Linux/macOS:

# export AWS_ACCESS_KEY_ID="your_key"
# export AWS_SECRET_ACCESS_KEY="your_secret"
# How to get AWS credentials
# Go to:

# AWS Console

# Then:

# Open IAM

# Create user

# Attach S3 permissions

# Create access key

# Copy credentials

# After configuring, test with:

# aws s3 ls
# If it lists buckets, your credentials work.


# def upload_to_s3(parquet_buffer):

#     s3_client = boto3.client(
#         "s3",
#         region_name=AWS_REGION
#     )

#     now = datetime.now()

#     timestamp = now.strftime("%Y%m%d_%H%M%S")

#     # Partitioned path
#     s3_key = (
#         f"{S3_PREFIX}/"
#         f"year={now.year}/"
#         f"month={now.month:02d}/"
#         f"day={now.day:02d}/"
#         f"transactions_{timestamp}.parquet"
#     )

#     s3_client.upload_fileobj(
#         parquet_buffer,
#         S3_BUCKET,
#         s3_key
#     )

# Your function is correct structurally.
# The error occurs because boto3.client() cannot find AWS credentials on your machine.

# You can fix it by adding credentials directly:

# import boto3
# from datetime import datetime

# def upload_to_s3(parquet_buffer):

#     s3_client = boto3.client(
#         "s3",
#         aws_access_key_id="YOUR_ACCESS_KEY",
#         aws_secret_access_key="YOUR_SECRET_KEY",
#         region_name=AWS_REGION
#     )

#     now = datetime.now()

#     timestamp = now.strftime("%Y%m%d_%H%M%S")

#     s3_key = (
#         f"{S3_PREFIX}/"
#         f"year={now.year}/"
#         f"month={now.month:02d}/"
#         f"day={now.day:02d}/"
#         f"transactions_{timestamp}.parquet"
#     )

#     s3_client.upload_fileobj(
#         parquet_buffer,
#         S3_BUCKET,
#         s3_key
#     )

#     print("Upload successful!")
# But for real projects, better approach is:

# aws configure
# Then keep your original code unchanged.

# Also ensure:

# parquet_buffer.seek(0)
# before upload, otherwise upload may send an empty file.

# Example:

# parquet_buffer.seek(0)

# s3_client.upload_fileobj(
#     parquet_buffer,
#     S3_BUCKET,
#     s3_key
# )
# Without seek(0), the buffer cursor may already be at the end.


# @bank_router.get("/accounts")
# @limiter.limit("2/minute")  
# def get_accounts(request: Request, db: Depends = Depends(get_db)):
#     cursor = db.cursor()
#     cursor.execute(f"SELECT * FROM {SCHEMA}.account;")
#     accounts = cursor.fetchall()
#     cursor.close()
#     return {"accounts": accounts}

# # --- BRANCH ENDPOINT ---
# @bank_router.get("/branches")
# @limiter.limit("2/minute")  
# def get_branches(request: Request, db: Depends = Depends(get_db)):
#     cursor = db.cursor()
#     cursor.execute(f"SELECT * FROM {SCHEMA}.branch;")
#     branches = cursor.fetchall()
#     cursor.close()
#     return {"branches": branches}

# # --- CARD ENDPOINT ---
# @bank_router.get("/cards")
# @limiter.limit("2/minute")  
# def get_cards(request: Request, db: Depends = Depends(get_db)):
#     cursor = db.cursor()
#     cursor.execute(f"SELECT * FROM {SCHEMA}.card;")
#     cards = cursor.fetchall()
#     cursor.close()
#     return {"cards": cards}

# # --- CUSTOMER ENDPOINT ---
# @bank_router.get("/customers")
# @limiter.limit("2/minute")  
# def get_customers(request: Request, db: Depends = Depends(get_db)):
#     cursor = db.cursor()
#     cursor.execute(f"SELECT * FROM {SCHEMA}.customer;")
#     customers = cursor.fetchall()
#     cursor.close()
#     return {"customers": customers}

# # --- PRODUCT ENDPOINT ---
# @bank_router.get("/products")
# @limiter.limit("2/minute")  
# def get_products(request: Request, db: Depends = Depends(get_db)):
#     cursor = db.cursor()
#     cursor.execute(f"SELECT * FROM {SCHEMA}.product;")
#     products = cursor.fetchall()
#     cursor.close()
#     return {"products": products} now for make a parquet file for every endpint like prev in different aws directory as per their table name suggest..  for these value also add the logic of incremental load caseu every day we will be running out pipeline and things should be strored in same place

# A good architecture is:

# FastAPI Endpoint
#       ↓
# Fetch JSON data
#       ↓
# Convert to Polars DataFrame
#       ↓
# Write to Parquet buffer
#       ↓
# Upload to S3
#       ↓
# Store in partitioned folders
# Since your pipeline runs daily, use:

# s3://bucket/bronze/accounts/year=2026/month=05/day=20/
# Same for every table.

# Recommended S3 structure:

# bronze/
#     accounts/
#     branches/
#     cards/
#     customers/
#     products/
# Inside each:

# year=2026/
#     month=05/
#         day=20/
# Create a reusable pipeline function.

# Example:

# import requests
# import polars as pl
# import boto3
# from io import BytesIO
# from datetime import datetime

# AWS_REGION = "us-east-1"
# S3_BUCKET = "your-bucket-name"
# BASE_PREFIX = "bronze"

# ENDPOINTS = {
#     "accounts": "http://localhost:8000/accounts",
#     "branches": "http://localhost:8000/branches",
#     "cards": "http://localhost:8000/cards",
#     "customers": "http://localhost:8000/customers",
#     "products": "http://localhost:8000/products"
# }
# Fetch → Convert → Upload:

# def process_endpoint(table_name, url):

#     print(f"Fetching {table_name} data...")

#     response = requests.get(url)

#     data = response.json()

#     records = data[table_name]

#     print("Creating Polars DataFrame...")

#     df = pl.DataFrame(records, strict=False)

#     parquet_buffer = BytesIO()

#     print("Writing parquet...")

#     df.write_parquet(parquet_buffer)

#     parquet_buffer.seek(0)

#     upload_to_s3(parquet_buffer, table_name)

#     print(f"{table_name} uploaded successfully!")
# Dynamic upload function:

# def upload_to_s3(parquet_buffer, table_name):

#     s3_client = boto3.client(
#         "s3",
#         region_name=AWS_REGION
#     )

#     now = datetime.now()

#     timestamp = now.strftime("%Y%m%d_%H%M%S")

#     s3_key = (
#         f"{BASE_PREFIX}/"
#         f"{table_name}/"
#         f"year={now.year}/"
#         f"month={now.month:02d}/"
#         f"day={now.day:02d}/"
#         f"{table_name}_{timestamp}.parquet"
#     )

#     s3_client.upload_fileobj(
#         parquet_buffer,
#         S3_BUCKET,
#         s3_key
#     )

#     print(f"Uploaded to {s3_key}")
# Run all pipelines:

# for table_name, url in ENDPOINTS.items():

#     try:
#         process_endpoint(table_name, url)

#     except Exception as e:
#         print(f"Pipeline failed for {table_name}: {e}")
# This design supports incremental loading automatically because:

# every run creates a new parquet file

# stored by date partitions

# old data remains untouched

# scalable for data lake architecture

# Example generated path:

# bronze/accounts/year=2026/month=05/day=20/accounts_20260520_201530.parquet
# This is standard Medallion/Data Lake style architecture used in Spark, Snowflake, Databricks, and modern data engineering systems.


# no no add as a one big table format for evey table in s3 cause there dont get much bigger values like our transaction table gets so keep a single loacation but add some metadata like data and other , and for day one /customer day to add new customer in same loc using incremental load

# Then your use case is better suited for:

# One parquet dataset per table
# Appending new records daily
# Instead of:

# partitioned folders by year/month/day
# Use:

# bronze/customers/customers.parquet
# bronze/accounts/accounts.parquet
# bronze/cards/cards.parquet
# and every day:

# fetch new data

# merge with old parquet

# remove duplicates

# overwrite same parquet file

# This is incremental append/upsert style loading.

# Recommended structure:

# bronze/
#     customers/customers.parquet
#     accounts/accounts.parquet
#     cards/cards.parquet
#     branches/branches.parquet
#     products/products.parquet
# Add metadata columns:

# loaded_at
# pipeline_run_date
# source
# Example:

# customer_id | name | loaded_at | pipeline_run_date
# Recommended logic:

# 1. Fetch API data
# 2. Create DataFrame
# 3. Add metadata columns
# 4. Download existing parquet from S3
# 5. Merge old + new
# 6. Remove duplicates using primary key
# 7. Upload updated parquet back to S3
# Example complete approach:

# import boto3
# import polars as pl
# import requests

# from io import BytesIO
# from datetime import datetime
# from botocore.exceptions import ClientError
# Upload incremental parquet:

# def incremental_upload(table_name, df, primary_key):

#     s3_client = boto3.client(
#         "s3",
#         region_name=AWS_REGION
#     )

#     s3_key = f"bronze/{table_name}/{table_name}.parquet"

#     now = datetime.now()

#     # Metadata columns
#     df = df.with_columns([
#         pl.lit(now.isoformat()).alias("loaded_at"),
#         pl.lit(now.date().isoformat()).alias("pipeline_run_date"),
#         pl.lit("fastapi").alias("source")
#     ])

#     try:
#         # Download existing parquet
#         obj = s3_client.get_object(
#             Bucket=S3_BUCKET,
#             Key=s3_key
#         )

#         existing_df = pl.read_parquet(
#             BytesIO(obj["Body"].read())
#         )

#         # Merge old + new
#         combined_df = pl.concat(
#             [existing_df, df],
#             how="vertical"
#         )

#         # Remove duplicates
#         combined_df = combined_df.unique(
#             subset=[primary_key],
#             keep="last"
#         )

#     except ClientError:
#         # First time load
#         combined_df = df

#     parquet_buffer = BytesIO()

#     combined_df.write_parquet(parquet_buffer)

#     parquet_buffer.seek(0)

#     s3_client.upload_fileobj(
#         parquet_buffer,
#         S3_BUCKET,
#         s3_key
#     )

#     print(f"{table_name} incremental load complete")
# Pipeline execution:

# TABLES = {
#     "customers": {
#         "url": "http://localhost:8000/customers",
#         "primary_key": "customer_id"
#     },
#     "accounts": {
#         "url": "http://localhost:8000/accounts",
#         "primary_key": "account_id"
#     }
# }
# Run:

# for table_name, config in TABLES.items():

#     response = requests.get(config["url"])

#     data = response.json()[table_name]

#     df = pl.DataFrame(data, strict=False)

#     incremental_upload(
#         table_name,
#         df,
#         config["primary_key"]
#     )
# Result:

# Day 1:

# customers.parquet
# 100 customers
# Day 2:

# 105 customers
# Only new customers added.

# If existing customer changed:

# keep="last"
# updates latest record automatically.

# This is a lightweight data lake incremental ingestion pattern.


# write full fledge prod code for with like bronz/ add (customer, account and others )

# import os
# from io import BytesIO
# from datetime import datetime

# import boto3
# import polars as pl
# import requests

# from botocore.exceptions import ClientError


# # =========================================================
# # CONFIG
# # =========================================================

# AWS_REGION = "us-east-1"
# S3_BUCKET = "your-bucket-name"

# BASE_API_URL = "http://localhost:8000"

# BRONZE_LAYER = "bronze"


# # =========================================================
# # TABLE CONFIGURATION
# # =========================================================

# TABLES = {
#     "customers": {
#         "endpoint": "/customers",
#         "primary_key": "customer_id"
#     },
#     "accounts": {
#         "endpoint": "/accounts",
#         "primary_key": "account_id"
#     },
#     "branches": {
#         "endpoint": "/branches",
#         "primary_key": "branch_id"
#     },
#     "cards": {
#         "endpoint": "/cards",
#         "primary_key": "card_id"
#     },
#     "products": {
#         "endpoint": "/products",
#         "primary_key": "product_id"
#     }
# }


# # =========================================================
# # S3 CLIENT
# # =========================================================

# s3_client = boto3.client(
#     "s3",
#     region_name=AWS_REGION
# )


# # =========================================================
# # FETCH DATA FROM API
# # =========================================================

# def fetch_api_data(table_name: str, endpoint: str):

#     url = f"{BASE_API_URL}{endpoint}"

#     print(f"\nFetching data from: {url}")

#     response = requests.get(url)

#     response.raise_for_status()

#     json_data = response.json()

#     records = json_data[table_name]

#     return records


# # =========================================================
# # CREATE POLARS DATAFRAME
# # =========================================================

# def create_dataframe(records):

#     df = pl.DataFrame(records, strict=False)

#     current_time = datetime.utcnow()

#     df = df.with_columns([

#         pl.lit(current_time.isoformat()).alias("loaded_at"),

#         pl.lit(current_time.date().isoformat())
#         .alias("pipeline_run_date"),

#         pl.lit("fastapi")
#         .alias("data_source")
#     ])

#     return df


# # =========================================================
# # DOWNLOAD EXISTING PARQUET FROM S3
# # =========================================================

# def load_existing_parquet(s3_key):

#     try:

#         response = s3_client.get_object(
#             Bucket=S3_BUCKET,
#             Key=s3_key
#         )

#         parquet_bytes = response["Body"].read()

#         existing_df = pl.read_parquet(
#             BytesIO(parquet_bytes)
#         )

#         print("Existing parquet found in S3")

#         return existing_df

#     except ClientError as e:

#         error_code = e.response["Error"]["Code"]

#         if error_code == "NoSuchKey":

#             print("No existing parquet found")

#             return None

#         raise


# # =========================================================
# # MERGE + REMOVE DUPLICATES
# # =========================================================

# def merge_incremental_data(
#     existing_df,
#     new_df,
#     primary_key
# ):

#     if existing_df is None:
#         return new_df

#     combined_df = pl.concat(
#         [existing_df, new_df],
#         how="vertical_relaxed"
#     )

#     combined_df = combined_df.unique(
#         subset=[primary_key],
#         keep="last"
#     )

#     return combined_df


# # =========================================================
# # UPLOAD TO S3
# # =========================================================

# def upload_parquet_to_s3(df, s3_key):

#     parquet_buffer = BytesIO()

#     df.write_parquet(
#         parquet_buffer,
#         compression="snappy"
#     )

#     parquet_buffer.seek(0)

#     s3_client.upload_fileobj(
#         parquet_buffer,
#         S3_BUCKET,
#         s3_key
#     )

#     print(f"Uploaded successfully -> {s3_key}")


# # =========================================================
# # PROCESS SINGLE TABLE
# # =========================================================

# def process_table(
#     table_name,
#     endpoint,
#     primary_key
# ):

#     print("\n" + "=" * 60)
#     print(f"PROCESSING TABLE: {table_name}")
#     print("=" * 60)

#     try:

#         # ---------------------------------------------
#         # STEP 1: FETCH DATA
#         # ---------------------------------------------

#         records = fetch_api_data(
#             table_name,
#             endpoint
#         )

#         print(f"Fetched {len(records)} records")


#         # ---------------------------------------------
#         # STEP 2: CREATE DATAFRAME
#         # ---------------------------------------------

#         new_df = create_dataframe(records)

#         print("Polars DataFrame created")


#         # ---------------------------------------------
#         # STEP 3: DEFINE S3 PATH
#         # ---------------------------------------------

#         s3_key = (
#             f"{BRONZE_LAYER}/"
#             f"{table_name}/"
#             f"{table_name}.parquet"
#         )

#         print(f"S3 Key: {s3_key}")


#         # ---------------------------------------------
#         # STEP 4: LOAD EXISTING DATA
#         # ---------------------------------------------

#         existing_df = load_existing_parquet(
#             s3_key
#         )


#         # ---------------------------------------------
#         # STEP 5: MERGE INCREMENTAL DATA
#         # ---------------------------------------------

#         final_df = merge_incremental_data(
#             existing_df,
#             new_df,
#             primary_key
#         )

#         print(
#             f"Final row count: {final_df.height}"
#         )


#         # ---------------------------------------------
#         # STEP 6: UPLOAD TO S3
#         # ---------------------------------------------

#         upload_parquet_to_s3(
#             final_df,
#             s3_key
#         )

#         print(f"{table_name} pipeline completed")


#     except Exception as e:

#         print(f"Pipeline failed for {table_name}")
#         print(f"Error: {e}")


# # =========================================================
# # MAIN PIPELINE
# # =========================================================

# def run_pipeline():

#     print("\nSTARTING BRONZE LAYER PIPELINE")

#     for table_name, config in TABLES.items():

#         process_table(
#             table_name=table_name,
#             endpoint=config["endpoint"],
#             primary_key=config["primary_key"]
#         )

#     print("\nPIPELINE FINISHED")


# # =========================================================
# # ENTRY POINT
# # =========================================================

# if __name__ == "__main__":

#     run_pipeline()


from utils import fetch_and_process_table

if __name__ == "__main__":
    fetch_and_process_table(
        table_name="customers",
        endpoint="/customers",
        primary_key="cust_id"
    )
