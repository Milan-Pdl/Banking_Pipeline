import requests
import polars as pl
import boto3

from io import BytesIO
from datetime import datetime
from config import SECERET_ACCESS_KEY,ACCESS_KEY,AWS_REGION


API_URL = "http://localhost:8000/api/bank/transactions"



S3_BUCKET = "milan-aafno-project"
S3_PREFIX = "bronze/transactions"

AWS_REGION = AWS_REGION



def fetch_transactions():

    response = requests.get(
        API_URL
    )

    response.raise_for_status()

    payload = response.json()



    transactions = payload.get("transactions", [])

    return transactions




def build_polars_dataframe(transactions):

    if not transactions:
        return None

    df = pl.DataFrame(transactions,strict=False)

    # Optional transformations
    # if "transaction_date" in df.columns:
    #     df = df.with_columns(
    #         pl.col("transaction_date").str.to_datetime(strict=False)
    #     )

    return df


#

def dataframe_to_parquet_buffer(df):

    parquet_buffer = BytesIO()

    df.write_parquet(
        parquet_buffer,
        compression="snappy"
    )

    parquet_buffer.seek(0)

    return parquet_buffer




def upload_to_s3(parquet_buffer):

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECERET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    now = datetime.now()

    timestamp = now.strftime("%Y%m%d_%H%M%S")

    s3_key = (
        f"{S3_PREFIX}/"
        f"year={now.year}/"
        f"month={now.month:02d}/"
        f"day={now.day:02d}/"
        f"transactions_{timestamp}.parquet"
    )

    s3_client.upload_fileobj(
        parquet_buffer,
        S3_BUCKET,
        s3_key
    )

    print("Upload successful!")
    print(f"Uploaded successfully: s3://{S3_BUCKET}/{s3_key}")



def main():

    try:

        print("Fetching transaction data from API...")

        transactions = fetch_transactions()

        if not transactions:
            print("No transactions found.")
            return

        print(f"Fetched {len(transactions)} transactions")

        print("Creating Polars DataFrame...")

        df = build_polars_dataframe(transactions)

        print("Converting to parquet...")

        parquet_buffer = dataframe_to_parquet_buffer(df)

        print("Uploading parquet file to S3...")

        upload_to_s3(parquet_buffer)

        print("Pipeline completed successfully.")

    except Exception as e:

        print(f"Pipeline failed: {str(e)}")


if __name__ == "__main__":
    main()