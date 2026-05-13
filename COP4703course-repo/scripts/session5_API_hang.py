import os
import time
import sqlalchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 1. Setup Connection
load_dotenv()
DB_HOST = os.getenv("POSTGRES_HOST")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def run_demonstration():
    print("--- Starting Database Performance Lab ---")
    
    with engine.connect() as conn:
        # --- PHASE 1: THE FAST QUERY ---
        print("\nTask 1: Rapid Metadata Check...")
        start = time.time()
        conn.execute(text("SELECT 1"))
        print(f"Result: Connection successful. (Time: {time.time() - start:.4f}s)")

        # --- PHASE 2: THE SIMULATED HANG ---
        print("\nTask 2: Fetching 50,000 rows (Simulating Network/Logic Hang)...")
        start = time.time()
        
        # We simulate the 'hang' by pausing the execution
        # In a real app, this represents a slow external API call or unoptimized code
        time.sleep(2) 
        
        # Now we actually hit the database
        result = conn.execute(text("SELECT COUNT(*) FROM calendar_data")).fetchone()
        
        duration = time.time() - start
        print(f"Result: {result[0]} rows processed.")
        print(f"CRITICAL HANG DETECTED: Execution took {duration:.2f} seconds.")

if __name__ == "__main__":
    try:
        run_demonstration()
    except Exception as e:
        print(f"Error connecting to database: {e}")