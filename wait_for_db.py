import time
import psycopg2

while True:
    try:
        conn = psycopg2.connect(
            dbname="notes_db",
            user="postgres",
            password="postgres",
            host="db",
            port="5432"
        )
        conn.close()
        print("DB is ready!")
        break
    except psycopg2.OperationalError:
        print("Waiting for DB...")
        time.sleep(2)