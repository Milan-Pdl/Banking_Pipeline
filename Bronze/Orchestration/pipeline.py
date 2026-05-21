from Bronze import accounts_into_s3
from Bronze import branches_into_s3
from Bronze import cards_into_s3
from Bronze import products_int_s3
from Bronze import transactions_to_s3


def run_pipeline():

    print("--------running----------------")

    accounts_into_s3.fetch_and_process_table(
        table_name="accounts",
        endpoint="/accounts",
        primary_key="account_id"
    )

    branches_into_s3.fetch_and_process_table(
        table_name="branches",
        endpoint="/branches",
        primary_key="branch_id"
    )

    cards_into_s3.fetch_and_process_table(
        table_name="cards",
        endpoint="/cards",
        primary_key="card_number"
    )

    products_int_s3.fetch_and_process_table(
        table_name="products",
        endpoint="/products",
        primary_key="product_id"
    )

    transactions_to_s3.main()

if __name__=="__main__":
    run_pipeline()   