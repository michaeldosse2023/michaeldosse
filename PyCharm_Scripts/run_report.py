# run_report.py
import pandas as pd
import data_utils
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    # Pull the folder path from your .env vault
    data_folder = os.getenv("DATA_FOLDER", "data/")

    # 1. Target the specific file
    target_file = os.path.join(data_folder, 'retail_sales.csv')

    if os.path.exists(target_file):
        print(f"🚀 Starting Morning Report for {target_file}...")

        # 2. Run the Engine
        raw_df = pd.read_csv(target_file)
        df_clean = data_utils.wash_and_dry(raw_df)

        # 3. Print the Intelligence
        data_utils.get_intelligence_snapshot(df_clean)

        print("\n✅ Report Complete. Ready for the Executive Board.")
    else:
        print(f"❌ Error: Could not find {target_file} in the data folder.")


if __name__ == "__main__":
    main()