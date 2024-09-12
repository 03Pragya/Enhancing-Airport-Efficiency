import psycopg2
import pandas as pd
import Utils.config as config
import Utils.postgress_queries as pg_queries



def getAirTrafficLandingData():
    pg_conn_params = config.POSTGRES_CONFIG

    pg_connection = psycopg2.connect(**pg_conn_params)
    
    # Check if the table exists
    with pg_connection.cursor() as cursor:
        cursor.execute(pg_queries.PG_CHECK_IF_LANDING_EXISTS)
        table_exists = cursor.fetchone()[0]

    if table_exists:
        df = pd.read_sql_query(pg_queries.PG_FETCH_FROM_LANDING, pg_connection)
    else:
        print(f"Table '{pg_queries.PG_LANDING_TABLE_NAME}' does not exist.")
        df = pd.DataFrame()  # or handle accordingly

    pg_connection.close()
    return df


def getAirTrafficPassengerData():
    pg_conn_params = config.POSTGRES_CONFIG

    pg_connection = psycopg2.connect(**pg_conn_params)
    df = pd.read_sql_query(pg_queries.PG_FETCH_FROM_PASSENGER, pg_connection)
    pg_connection.close()
    return df
