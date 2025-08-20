import os
import pandas as pd
from io import BytesIO
from minio import Minio
from pymongo import MongoClient
from prefect import flow, task

# ----------------------------
# Environment variables
# ----------------------------
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")
CSV_OBJECT_NAME = os.getenv("CSV_OBJECT_NAME")

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

# -------------------------
# MongoDB Connection
#--------------------------
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


# ----------------------------
# Tasks
# ----------------------------
@task
def fetch_csv_from_minio() -> pd.DataFrame:
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False  # Currently using local system, change to True if using HTTPS
    )
    
    data = client.get_object(MINIO_BUCKET, CSV_OBJECT_NAME)
    df = pd.read_csv(data)
    data.close()
    data.release_conn()
    return df

@task
def transform_to_list(df: pd.DataFrame):
    return df.to_dict("records")

@task
def load_to_mongodb(data: list):
    if data:
        collection.insert_many(data)
    client.close()
    return len(data)


# ----------------------------
# Prefect flow
# ----------------------------
@flow(name="MinIO to MongoDB ETL")
def minio_to_mongo_etl():
    df = fetch_csv_from_minio()
    transformed_data = transform_to_list(df)
    count = load_to_mongodb(transformed_data)
    print(f"Inserted {count} records into MongoDB")


# Run flow when container starts
if __name__ == "__main__":
    minio_to_mongo_etl()
