import pandas as pd
from typing import List, Dict, Any

class SteamDataTransformer:
    """
    Class responsible for cleaning and transforming raw Steam telemetry data
    using pandas, preparing it for data warehouse storage.
    """
    
    def __init__(self, game_mapping: Dict[int, str]):
        """
        Initializes the transformer with a mapping dictionary to enrich the data.
        
        Args:
            game_mapping (Dict[int, str]): A dictionary mapping App IDs to Game Names.
        """
        self.game_mapping = game_mapping
        print("⚙️ SteamDataTransformer successfully initialized.")

    def transform(self, raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Transforms a list of raw dictionaries into a clean, structured pandas DataFrame.
        """
        if not raw_data:
            print("⚠️ Warning: No raw data provided for transformation.")
            return pd.DataFrame()

        print("🔄 Starting data transformation process...")
        
        # 1. Load data into a pandas DataFrame
        df = pd.DataFrame(raw_data)
        
        # 2. Data Enrichment: Map App IDs to human-readable Game Names
        # This simulates joining a fact table with a dimension table in a Data Warehouse
        df['game_name'] = df['app_id'].map(self.game_mapping)
        
        # 3. Type Conversion: Ensure timestamp is a proper datetime object, not just a string
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 4. Data Quality Check: Handle missing values
        # If an app_id wasn't found in our mapping dictionary, fill it with 'Unknown'
        df['game_name'] = df['game_name'].fillna('Unknown')
        
        # 5. Schema Enforcement: Reorder columns for a cleaner final table structure
        df = df[['timestamp', 'app_id', 'game_name', 'player_count']]
        
        print("✅ Data transformation complete. DataFrame is ready.")
        return df
