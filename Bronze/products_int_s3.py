from utils import fetch_and_process_table

if __name__ == "__main__":
    fetch_and_process_table(
        table_name="products",
        endpoint="/products",
        primary_key="product_id"
    )