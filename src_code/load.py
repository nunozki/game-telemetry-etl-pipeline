import sqlite3
import pandas as pd
from typing import Optional

class SteamDataLoader:
    """
    Class responsible for loading transformed data into a SQL Database.
    Simulates a Data Warehouse load process.
    """
    
    def __init__(self, db_name: str = "steam_telemetry.db"):
        """
        Initializes the database connection.
        
        Args:
            db_name (str): The name of the SQLite database file.
        """
        self.db_name = db_name
        # The connection will be opened and closed when needed to avoid locking issues
        print(f"🗄️ SteamDataLoader initialized. Target Database: {self.db_name}")

    def create_table_if_not_exists(self) -> None:
        """
        Executes a raw SQL DDL (Data Definition Language) statement to ensure 
        our target table exists before we try to insert data.
        """
        # Writing raw SQL proves you understand database schemas and data types
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS daily_player_counts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            app_id INTEGER NOT NULL,
            game_name TEXT NOT NULL,
            player_count INTEGER NOT NULL
        );
        """
        try:
            # Context manager (with) ensures the connection closes automatically even if it crashes
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(create_table_sql)
                conn.commit()
                print("✅ SQL Schema verified: Table 'daily_player_counts' is ready.")
        except sqlite3.Error as e:
            print(f"❌ SQL Database error during table creation: {e}")

    def load_dataframe(self, df: pd.DataFrame, table_name: str = "daily_player_counts") -> bool:
        """
        Loads the pandas DataFrame into the SQL database.
        
        Args:
            df (pd.DataFrame): The transformed data.
            table_name (str): The target SQL table.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if df.empty:
            print("⚠️ Warning: DataFrame is empty. Nothing to load to SQL.")
            return False

        print(f"💾 Loading {len(df)} rows into SQL table '{table_name}'...")
        
        try:
            with sqlite3.connect(self.db_name) as conn:
                # pandas to_sql is the industry standard for bulk inserts
                # if_exists='append' ensures we add new data without deleting the old one
                df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
                print("✅ Data successfully loaded into the SQL database.")
                return True
        except ValueError as ve:
            print(f"❌ Value Error during SQL load: {ve}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during SQL load: {e}")
            return False

    def run_validation_query(self) -> None:
        """
        Executes a raw SQL SELECT query to validate the inserted data.
        Proves capability to write analytical SQL queries.
        """
        validation_sql = """
        SELECT game_name, MAX(player_count) as peak_players, COUNT(*) as total_records
        FROM daily_player_counts
        GROUP BY game_name
        ORDER BY peak_players DESC;
        """
        
        print("\n🔎 Running SQL Validation Query (Top Games by Peak Players):")
        try:
            with sqlite3.connect(self.db_name) as conn:
                # We can use pandas to execute the SQL query and format the output beautifully
                result_df = pd.read_sql_query(validation_sql, conn)
                print(result_df.to_string(index=False))
        except sqlite3.Error as e:
            print(f"❌ SQL Database error during validation: {e}")