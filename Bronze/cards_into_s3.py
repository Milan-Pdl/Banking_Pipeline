from utils import fetch_and_process_table

if __name__ == "__main__":
    fetch_and_process_table(
        table_name="cards",
        endpoint="/cards",
        primary_key="card_id"
    )