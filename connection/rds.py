from os import system
import psycopg2
import boto3


def RdsConnection()->None:
    password = "ampify1922"
    conn = None
    
    try:
        conn = psycopg2.connect(
            host='ampify-1.congww0qs201.us-east-1.rds.amazonaws.com',
            port=5432,
            database='postgres',
            user='ampify1922',
            password=password,
            sslmode='verify-full',
        sslrootcert='../certs/global-bundle.pem'
        )
        cur = conn.cursor()
        cur.execute('SELECT version();')
        print(cur.fetchone()[0])
        cur.close()
    except Exception as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()
RdsConnection()