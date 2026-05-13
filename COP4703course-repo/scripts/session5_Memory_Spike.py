import os
import random
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)

def seed_100k():
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    print("Seeding 100,000 rows...")
    
    with engine.begin() as conn:
        # Clear existing data first
        conn.execute(text("TRUNCATE TABLE calendar_data"))
        
        # Batch insert for speed
        for i in range(10):  # 10 batches of 10,000
            data = [{"month_name": random.choice(months), "day_number": random.randint(1, 28)} for _ in range(10000)]
            conn.execute(
                text("INSERT INTO calendar_data (month_name, day_number) VALUES (:month_name, :day_number)"),
                data
            )
            print(f"Inserted {(i+1)*10000} rows...")

if __name__ == "__main__":
    seed_100k()