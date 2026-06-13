import time
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

while True:
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        print("DB is ready!")
        break
    except psycopg2.OperationalError:
        print("Waiting for DB...")
        time.sleep(2)