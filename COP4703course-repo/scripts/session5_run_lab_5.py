import os
import time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()
class CalendarData(Base):
    __tablename__ = "calendar_data"
    id = Column(Integer, primary_key=True)
    month_name = Column(String)
    day_number = Column(Integer)

def run_experiment(method="all"):
    session = Session()
    print(f"\n--- Testing Method: {method} ---")
    
    try:
        if method == "all":
            # 2. FAIL: .all() loads EVERYTHING into RAM at once
            results = session.execute(select(CalendarData)).scalars().all()
            print(f"Successfully loaded {len(results)} items into memory.")
        
        elif method == "yield":
            # 3. REFACTOR: yield_per() streams data in chunks (low RAM)
            print("Streaming rows in batches of 1000...")
            # We use execution_options to tell the driver to stream
            stmt = select(CalendarData).execution_options(yield_per=1000)
            
            counter = 0
            for row in session.execute(stmt).scalars():
                counter += 1
                if counter % 10000 == 0:
                    print(f"Processed {counter} rows...")
            print(f"Successfully processed {counter} items via streaming.")

    except Exception as e:
        print(f"CRASHED! Reason: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    choice = input("Enter 'all' to watch it crash or 'yield' to watch it survive: ").strip().lower()
    run_experiment(choice)