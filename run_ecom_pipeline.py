import os
import pandas as pd
from dotenv import load_dotenv
import data_utils
import ecom_analysis

# 1. Load the Secure Vault
load_dotenv()
input_path = os.getenv("ECOM_DATA_PATH")
output_path = os.getenv("ECOM_OUTPUT_PATH")

print("🚀 Initializing Ecommerce Automation Pipeline...")

try:
    # 2. Extract Data
    df = pd.read_csv(input_path, encoding='cp1252')

    # 3. Transform Data
    df = data_utils.clean_ecom_titles(df)

    if 'order_date' in df.columns:
        df['order_date'] = df['order_date'].apply(data_utils.format_date)

    if 'order_id' in df.columns:
        df = df.drop_duplicates(subset=['order_id'], keep='first')

    # Note: If your column name is different (e.g. 'payment_method'), pass it here!
    df = data_utils.flag_customer_status(df, payment_column='payment_details')

    # 4. Analyze Data (The Snapshot)
    ecom_analysis.generate_ecom_snapshot(df)

    # 5. Export Masterpiece
    df.to_csv(output_path, index=False)
    print(f"💾 Cleaned dataset successfully exported to: {output_path}")
    print("🏁 Pipeline execution completed perfectly.")

except Exception as e:
    print(f"❌ Pipeline Failed: {str(e)}")