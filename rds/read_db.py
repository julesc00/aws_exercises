# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import boto3
import json
import psycopg2
import time
from botocore.exceptions import ClientError
from psycopg2 import sql

def list_rds_tables(host, database, user, password, port=5432, schema='public'):
    try:
        # Connect to your PostgreSQL database on RDS
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )

        # Create a cursor object
        cursor = conn.cursor()

        create_table_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS users_test (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)

        # Execute the SQL command
        cursor.execute(create_table_query)
        conn.commit()
        time.sleep(3)
        print("Table created successfully in PostgreSQL")


        # Execute the query to get table names from the specified schema
        query = "SELECT * FROM users_test"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        query_field_types = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'users_test';
        """
        cursor.execute(query_field_types)
        schema_info = cursor.fetchall()

        # Print the column names and data types
        for column in schema_info:
            print(f"Column: {column[0]}, Data Type: {column[1]}")

        cursor.execute(f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = '{schema}';
        """)

        # Fetch all the results
        tables = cursor.fetchall()

        # Print out the table names
        print(f"Tables in schema '{schema}':")
        for table in tables:
            print(table[0])

        if conn:
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")



def get_secret():

    secret_name = "rds!cluster-15579ad9-c7c6-4422-b187-315a3e5dd491"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    print(secret)
    dict_secret = json.loads(secret)
    return dict_secret




if __name__ == "__main__":
    creds = get_secret()
    # Your code goes here.

    host = 'database-1-instance-1.cfvzoakkcjeu.us-east-1.rds.amazonaws.com'
    database = 'postgres'
    user = creds['username']
    password = creds['password']
    print("Connecting to the database...")
    print(list_rds_tables(host, database, user, password))