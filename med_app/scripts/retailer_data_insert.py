# import sqlite3

# db_path = r"medical.db"

# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# cursor.execute("DELETE FROM retailers")  # Clear all rows

# conn.commit()
# conn.close()

# print("✅ All records cleared from 'retailers' table.")




import csv
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL

# Use synchronous engine
engine = create_engine("sqlite:///./medical.db", echo=True, future=True)

Base = declarative_base()

class RetailerDbModel(Base):
    __tablename__ = "retailers"

    retailer_id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String, nullable=True)
    owner_name = Column(String, nullable=True)
    gst_number = Column(String, nullable=True)
    license_number = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)
    address_line1 = Column(String, nullable=True)
    address_line2 = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    gps_latitude = Column(DECIMAL(10, 7), nullable=True)
    gps_longitude = Column(DECIMAL(10, 7), nullable=True)

# Create tables if not exist
# Base.metadata.create_all(bind=engine)

def insert_data_from_csv(csv_file_path):
    with Session(engine) as session, open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            retailer = RetailerDbModel(
                shop_name=row.get('shop_name'),
                address_line1=row.get('address_line1'),
                phone_number=row.get('phone_number'),
                gps_latitude=row.get('gps_latitude') or None,
                gps_longitude=row.get('gps_longitude') or None,
                owner_name=row.get('owner_name'),
                gst_number=row.get('gst_number'),
                license_number=row.get('license_number'),
                email=row.get('email'),
                password_hash=row.get('password_hash'),
                city=row.get('city'),
                state=row.get('state'),
                zip_code=row.get('zip_code'),
            )
            session.add(retailer)
        session.commit()

# Usage example
insert_data_from_csv(r"c:\Users\ajith\Downloads\merged_pharmacies_data.csv")


