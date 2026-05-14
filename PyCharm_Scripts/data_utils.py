# data_utils.py
import pandas as pd
from datetime import datetime


def wash_and_dry(df, current_date_str="2026-05-13"):
    """
    The Professional Cleaning Library
    - Handles headers, future dates, and nulls.
    """
    df_cleaned = df.copy()
    current_date = pd.to_datetime(current_date_str)

    # 1. Header Normalization (The Architect's First Rule)
    df_cleaned.columns = [col.strip().lower().replace(' ', '_') for col in df_cleaned.columns]

    # 2. Duplicate Column Removal
    df_cleaned = df_cleaned.loc[:, ~df_cleaned.columns.duplicated()]

    # 3. Dynamic Date Conversion & Future-Date Filtering
    date_keywords = ['date', 'joined', 'enrolment', 'time']
    for col in df_cleaned.columns:
        if any(key in col for key in date_keywords):
            df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
            # The 'Reality Check' filter you discovered
            df_cleaned = df_cleaned[df_cleaned[col] <= current_date]

    # 4. Handle Nulls (Applying your 'slow-completers' logic)
    # This ensures consistency across all future projects
    df_cleaned = df_cleaned.fillna('laggards')

    return df_cleaned

# *********** New Block of Codes at 14May PM ***************
def get_intelligence_snapshot(df):
    """
    Generates a high-level summary while handling 'laggards' in numeric columns.
    """
    # Create a numeric-only version of the columns for math
    # 'coerce' turns 'laggards' into NaN (ignored by sum/mean)
    sales_numeric = pd.to_numeric(df['sales_amount'], errors='coerce')
    profit_numeric = pd.to_numeric(df['profit'], errors='coerce')
    stock_numeric = pd.to_numeric(df['stock_quantity'], errors='coerce')

    stats = {
        "Total Revenue": sales_numeric.sum(),
        "Average Profit": profit_numeric.mean(),
        "Laggard Count": (df == 'laggards').sum().sum(),
        "Top Region": df['region'].value_counts().idxmax(),
        "Total Items in Stock": stock_numeric.sum()
    }

    print("--- 🧠 INTELLIGENCE SNAPSHOT ---")
    for key, value in stats.items():
        if isinstance(value, (float, int)):
            print(f"{key}: {value:,.2f}")
        else:
            print(f"{key}: {value}")
    print("--------------------------------")

    return stats