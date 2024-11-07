import os
import pymysql
import pandas as pd
from google.cloud.sql.connector import Connector

def init_connection_pool():
    """Initialize connection pool to Cloud SQL database"""
    
    instance_connection_name = os.environ.get("INSTANCE_CONNECTION_NAME")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS") 
    db_name = os.environ.get("DB_NAME")

    connector = Connector()

    def getconn():
        conn = connector.connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    return getconn

def test_query(query):
    """Execute a test query and return results"""
    conn = init_connection_pool()()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Get column names
            columns = [desc[0] for desc in cursor.description]
            
            # Convert to DataFrame
            df = pd.DataFrame(results, columns=columns)
            return df
            
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

def main():
    # Example test queries
    test_queries = [
        """
        SELECT * FROM `chess-com-data`.`super_gm_games_2024` LIMIT 10;
        """,
        
        """
        SELECT AVG(white_rating) as avg_rating
        FROM super_gm_games_2024 
        WHERE white_username = 'Hikaru'
        """
    ]
    
    for i, query in enumerate(test_queries):
        print(f"\nExecuting test query {i+1}:")
        print(query)
        results = test_query(query)
        if results is not None:
            print("\nResults:")
            print(results)
        print("-" * 50)

if __name__ == "__main__":
    main()
