PG_PASSENGER_TABLE_NAME = "airtrafficpassenger"
PG_LANDING_TABLE_NAME = "airtrafficlanding"
PG_PASSENGER_TABLE_CREATE = f"""
    CREATE TABLE IF NOT EXISTS {PG_PASSENGER_TABLE_NAME} (
        activity_period VARCHAR(10),
        activity_period_start_date TIMESTAMP,
        operating_airline VARCHAR(255),
        operating_airline_iata_code VARCHAR(10),
        published_airline VARCHAR(255),
        published_airline_iata_code VARCHAR(10),
        geo_summary VARCHAR(255),
        geo_region VARCHAR(255),
        activity_type_code VARCHAR(255),  -- Add this field
        price_category_code VARCHAR(255),  -- Add this field
        terminal VARCHAR(255),             -- Add this field
        boarding_area VARCHAR(255),         -- Add this field
        passenger_count INTEGER,
        data_as_of TIMESTAMP,
        data_loaded_at TIMESTAMP
    )
"""
PG_PASSENGER_ADD_DATA = f"""
            INSERT INTO {PG_PASSENGER_TABLE_NAME} (
                activity_period,
                activity_period_start_date,
                operating_airline,
                operating_airline_iata_code,
                published_airline,
                published_airline_iata_code,
                geo_summary,
                geo_region,
                activity_type_code,
                price_category_code,
                terminal,
                boarding_area,
                passenger_count,
                data_as_of,
                data_loaded_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
PG_CHECK_IF_LANDING_EXISTS = f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{PG_LANDING_TABLE_NAME}')"
PG_FETCH_FROM_LANDING = f"SELECT * FROM {PG_LANDING_TABLE_NAME}"
PG_FETCH_FROM_PASSENGER = f"SELECT * FROM {PG_PASSENGER_TABLE_NAME}"