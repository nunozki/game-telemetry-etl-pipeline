import sys
sys.path.append('../src_code')  # Ensure src is in the path for imports

from src_code.extract import SteamDataExtractor
from src_code.datatransformer import SteamDataTransformer
from src_code.load import SteamDataLoader
import pandas as pd

def run_etl_pipeline():
    """
    Main orchestration function for the Steam Telemetry ETL Pipeline.
    Executes the Extract, Transform, and Load phases sequentially.
    """
    print("🚀 Starting Steam Telemetry ETL Pipeline...\n")
    
    # 0. Configuration & Dimension Data (Target Games)
    target_games = {
        730: "Counter-Strike 2",
        570: "Dota 2",
        578080: "PUBG: BATTLEGROUNDS",
        1172470: "Apex Legends",
        252490: "Rust",
        271590: "Grand Theft Auto V"
    }
    
    # Target SQLite Database file
    db_name = "steam_telemetry.db"
    
    try:
        # ==========================================
        # PHASE 1: EXTRACT
        # ==========================================
        print("--- [PHASE 1: EXTRACT] ---")
        extractor = SteamDataExtractor(timeout=10)
        raw_data = extractor.extract_multiple_games(target_games)
        
        # Guard clause: Stop pipeline if extraction failed completely
        if not raw_data:
            print("❌ Pipeline stopped: No data extracted from the API.")
            sys.exit(1)
            
        print(f"✅ Phase 1 Complete. Extracted {len(raw_data)} records.\n")
        
        # ==========================================
        # PHASE 2: TRANSFORM
        # ==========================================
        print("--- [PHASE 2: TRANSFORM] ---")
        transformer = SteamDataTransformer(game_mapping=target_games)
        clean_df = transformer.transform(raw_data)
        
        # Guard clause: Stop pipeline if dataframe is empty after cleaning
        if clean_df.empty:
            print("❌ Pipeline stopped: Transformation resulted in an empty DataFrame.")
            sys.exit(1)
            
        print(f"✅ Phase 2 Complete. Transformed {len(clean_df)} rows successfully.\n")
        
        # ==========================================
        # PHASE 3: LOAD
        # ==========================================
        print("--- [PHASE 3: LOAD] ---")
        loader = SteamDataLoader(db_name=db_name)
        
        # Ensure the database schema exists before inserting
        loader.create_table_if_not_exists()
        
        # Load the data into the SQL database
        load_success = loader.load_dataframe(clean_df)
        
        if not load_success:
            print("❌ Pipeline stopped: Failed to load data into the database.")
            sys.exit(1)
        
        # Validate the load to ensure data integrity
        loader.run_validation_query()
        
        print("\n🎉 ETL Pipeline executed successfully!")
        
    except Exception as e:
        # Catch any unexpected critical errors that crash the pipeline
        print(f"\n💥 CRITICAL: Pipeline failed due to an unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_etl_pipeline()