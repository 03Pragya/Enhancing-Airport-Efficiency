#save csv file in postgresql

# Library
import psycopg2
import pandas as pd
import time
from sqlalchemy import create_engine, text
import pymongo
import json
from bson import json_util
import Utils.config as config
import apicall
import Utils.postgress_queries as pg_queries


def InsertCSVTODB():
    db_params = config.POSTGRES_CONFIG

    engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}')
    csv_path = "Air_Traffice_Landings_Statitics.csv"
    df = pd.read_csv(csv_path)
    df.to_sql("airtrafficlanding", engine, if_exists='replace', index=False)


def InsertJSONToMongo():
    '''Creates the Mongo client along with the collection that will be used'''
    client = pymongo.MongoClient(config.MONGODB_URI)
    db = client[config.MONGODB_DATABASE_NAME]
    collection = db[config.MONDGODB_COLLECTION_NAME]

    # Call API function and inserts data into MongoDB
    collection.insert_many(apicall.AirTrafficClient()) 

    # Close MongoDB connection
    client.close()

def ConvertJSONToCSV():
    pg_conn_params = config.POSTGRES_CONFIG

    # Connect to MongoDB
    mongo_client = pymongo.MongoClient(config.MONGODB_URI)
    mongo_db = mongo_client[config.MONGODB_DATABASE_NAME]
    mongo_collection = mongo_db[config.MONDGODB_COLLECTION_NAME]

    # Retrieve data from MongoDB collection
    mongo_data = list(mongo_collection.find())

    # Connect to PostgreSQL
    pg_connection = psycopg2.connect(**pg_conn_params)
    pg_cursor = pg_connection.cursor()

    # Create PostgreSQL table
    pg_cursor.execute(pg_queries.PG_PASSENGER_TABLE_CREATE)

    # Insert data into PostgreSQL table
    for document in mongo_data:
        pg_cursor.execute(pg_queries.PG_PASSENGER_ADD_DATA, (
            document.get("activity_period"),
            document.get("activity_period_start_date"),
            document.get("operating_airline"),
            document.get("operating_airline_iata_code"),
            document.get("published_airline"),
            document.get("published_airline_iata_code"),
            document.get("geo_summary"),
            document.get("geo_region"),
            document.get("activity_type_code"),
            document.get("price_category_code"),
            document.get("terminal"),
            document.get("boarding_area"),
            int(document.get("passenger_count", 0)),
            document.get("data_as_of"),
            document.get("data_loaded_at")
        ))

        # Commit changes and close connections
    pg_cursor.close()
    pg_connection.commit()
    pg_connection.close()
    mongo_client.close()