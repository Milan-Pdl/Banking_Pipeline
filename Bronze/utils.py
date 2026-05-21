import os
from io import BytesIO
from datetime import datetime
import boto3
import polars as pl
import requests
from botocore.exceptions import ClientError
from config import BUCKET_NAME,ACCESS_KEY,SECERET_ACCESS_KEY

# --- Configuration ---
AWS_REGION = "us-east-1"
S3_BUCKET = BUCKET_NAME  # Replace with your bucket
BASE_API_URL = "http://localhost:8000/api/bank"
BRONZE_LAYER = "bronze"

def get_s3_client():
        s3_client = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECERET_ACCESS_KEY,
        region_name=AWS_REGION
    )
        return s3_client

def fetch_and_process_table(table_name: str, endpoint: str, primary_key: str):
    """
    Core production engine to fetch API data, append metadata,
    upsert with existing Parquet data on S3, and save back to S3.
    """
    s3_client = get_s3_client()
    url = f"{BASE_API_URL}{endpoint}"
    s3_key = f"{BRONZE_LAYER}/{table_name}/{table_name}.parquet"
    
    print(f"\n{'='*50}\nInjesting Table: {table_name.upper()}\n{'='*50}")
    
    # Step 1: Fetch from API
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        records = response.json().get(table_name, [])
        print(f"[-] Successfully fetched {len(records)} records from API.")
    except Exception as e:
        print(f"[ERROR] Failed fetching data from {url}: {e}")
        return

    if not records:
        print(f"[-] No new records found for {table_name}. Skipping pipeline.")
        return

    # Step 2: Convert to Polars DataFrame & Inject Metadata
    # strict=False handles any unpredicted nulls/floats seamlessly
    new_df = pl.DataFrame(records, strict=False)
    
    current_time = datetime.now()
    new_df = new_df.with_columns([
        pl.lit(current_time.isoformat()).alias("loaded_at"),
        pl.lit(current_time.date().isoformat()).alias("pipeline_run_date"),
        pl.lit("fastapi").alias("data_source")
    ])

    # Step 3: Handle Incremental Upsert Logic (Read existing S3 file)
    existing_df = None
    try:
        s3_obj = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
        s3_obj = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
        print(f"-------------------{s3_obj}-----------------------")
        # print(f"-------------------{s3_obj[]}-----------------------")
        existing_df = pl.read_parquet(BytesIO(s3_obj["Body"].read()))
        print("[-] Found existing Parquet layer on S3. Merging datasets...")
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            print("[-] No existing dataset found. Initializing fresh baseline layer.")
        else:
            print(f"[ERROR] S3 breakdown while retrieving existing file: {e}")
            raise


    if existing_df is not None:
        # vertical_relaxed safely handles column ordering or minor type upcasts
        final_df = pl.concat([existing_df, new_df], how="vertical_relaxed")
            # Step 4: Vertical Concatenation & Primary Key Deduplication

            # take this example for understanding what is happening

            #     Existing S3 parquet (existing_df)
            # id	name
            # 1	    Ram
            # 2	    Hari
            # New   API data (new_df)
            # id	name
            # 2	    Hari Updated
            # 3	    Sita

            # After concat:

            # id	name
            # 1	    Ram
            # 2	    Hari
            # 2	    Hari Updated
            # 3	    Sita

            # So now both old and new records exist together.

            # keep last means keep the latest record
                #             Keep the newest/latest record.

                # So:

                # id	name
                # 1	    Ram
                # 2	    Hari Updated
                # 3	    Sita
                # The old Hari row is removed.
                
        final_df = final_df.unique(subset=[primary_key], keep="last")
    else:
        final_df = new_df

    # Step 5: Save optimized Parquet file straight back to S3
    try:
        parquet_buffer = BytesIO()
        final_df.write_parquet(parquet_buffer, compression="snappy")
        parquet_buffer.seek(0)

        s3_client.upload_fileobj(parquet_buffer, S3_BUCKET, s3_key)
        print(f"[SUCCESS] Upsert complete. Total rows in {s3_key}: {final_df.height}")
    except Exception as e:
        print(f"[ERROR] Failed to upload updated Parquet to S3: {e}")