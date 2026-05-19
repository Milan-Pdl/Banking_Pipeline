import psycopg2
from .dbconfig import PASSWORD,DATABASE,USER,HOST
class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating new database instance...")
            cls._instance = super().__new__(cls)

            # Create PostgreSQL connection once
            cls._connection = psycopg2.connect(
                host=HOST,
                port=5432,
                database=DATABASE,
                user=USER,
                password=PASSWORD
            )

        return cls._instance

    def get_connection(self):
        return self._connection



db1 = DatabaseConnection()
db2 = DatabaseConnection()
def get_db():
    try:
        yield db1.get_connection()
    except ConnectionError:
        print("failed connection")

get_db()

# print(db1 is db2)  

# conn = db1.get_connection()

# cursor = conn.cursor()
# cursor.execute("SELECT * from bank.transaction;")

# print(cursor.fetchone())

# cursor.close()

