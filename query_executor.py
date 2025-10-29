import psycopg2, os
import pandas as pd

def run_query(sql):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    df = pd.read_sql(sql, conn)
    conn.close()
    return df.to_dict(orient="records")
