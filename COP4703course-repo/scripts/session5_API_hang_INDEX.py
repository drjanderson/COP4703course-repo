import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)

def run_test():
    query = "SELECT * FROM calendar_data WHERE month_name = 'July' AND day_number = 15"
    
    with engine.connect() as conn:
        # 1. Cleanup: Ensure no index exists from previous runs
        conn.execute(text("DROP INDEX IF EXISTS idx_month_day"))
        conn.commit()

        # 2. PHASE 1: No Index (Sequential Scan)
        print("--- Phase 1: No Index ---")
        start = time.time()
        # We use EXPLAIN ANALYZE to get the DB's internal timing
        result_slow = conn.execute(text(f"EXPLAIN ANALYZE {query}"))
        for row in result_slow:
            print(row[0])
        print(f"Total Python-side time: {(time.time() - start)*1000:.2f} ms\n")

        # 3. Create the Index
        print("Creating B-Tree Index on (month_name, day_number)...")
        conn.execute(text("CREATE INDEX idx_month_day ON calendar_data(month_name, day_number)"))
        conn.commit()

        # 4. PHASE 2: With Index (Index Scan)
        print("--- Phase 2: With Index ---")
        start = time.time()
        result_fast = conn.execute(text(f"EXPLAIN ANALYZE {query}"))
        for row in result_fast:
            print(row[0])
        print(f"Total Python-side time: {(time.time() - start)*1000:.2f} ms")

if __name__ == "__main__":
    run_test()