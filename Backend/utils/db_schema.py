

def fetch_table_as_json(db, schema: str, table_name: str):
    cursor = db.cursor()

    # Step 1: Get column names
    cursor.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = '{schema}'
        AND table_name = '{table_name}'
        ORDER BY ordinal_position;
    """)

    columns = [row[0] for row in cursor.fetchall()]

    # Step 2: Fetch actual table data
    cursor.execute(f"SELECT * FROM {schema}.{table_name};")

    rows = cursor.fetchall()

    # Step 3: Convert tuples -> dictionaries
    data = [dict(zip(columns, row)) for row in rows]

    cursor.close()

    return data