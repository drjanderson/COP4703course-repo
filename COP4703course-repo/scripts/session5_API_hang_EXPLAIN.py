import os
import sqlalchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.getenv("POSTGRES_HOST")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def diagnose():
    query = "SELECT * FROM calendar_data WHERE month_name = 'July' AND day_number = 15"
    
    with engine.connect() as conn:
        print(f"--- Diagnosing Query ---\nQuery: {query}\n")
        
        # We wrap the query in EXPLAIN ANALYZE
        result = conn.execute(text(f"EXPLAIN ANALYZE {query}"))
        
        print("QUERY PLAN REPORT:")
        print("-" * 30)
        for row in result:
            # The result of an EXPLAIN query is a series of strings (the plan lines)
            print(row[0])
        print("-" * 30)

if __name__ == "__main__":
    diagnose()