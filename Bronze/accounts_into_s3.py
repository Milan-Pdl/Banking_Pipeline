from utils import fetch_and_process_table

if __name__ == "__main__":
    fetch_and_process_table(
        table_name="accounts",
        endpoint="/accounts",
        primary_key="account_id"
    )