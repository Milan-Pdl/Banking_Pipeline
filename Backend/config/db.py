import psycopg2

class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating new database instance...")
            cls._instance = super().__new__(cls)

            # Create PostgreSQL connection once
            cls._connection = psycopg2.connect(
                host="localhost",
                port=5432,
                database="BankDB",
                user="user",
                password="password"
            )

        return cls._instance

    def get_connection(self):
        return self._connection



db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(db1 is db2)  

conn = db1.get_connection()

cursor = conn.cursor()
cursor.execute("SELECT * from bank.transaction;")

print(cursor.fetchone())

cursor.close()

