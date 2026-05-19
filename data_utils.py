import pandas as pd
import re


def clean_ecom_titles(df):
    """Standardizes column names to lowercase and strips whitespaces."""
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    return df

def format_date(date_entry):
    """Cleans ordinal suffixes and formats dates to UK standard."""
    if pd.isna(date_entry) or str(date_entry).strip().lower() in ['none', '']:
        return ""
    date_str = str(date_entry)
    clean_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
    try:
        dt = pd.to_datetime(clean_date, dayfirst=True)
        return dt.strftime('%d/%m/%Y')
    except:
        return date_str


def flag_customer_status(df, payment_column='payment_details'):
    """
    Creates a customer_status column.
    Flags rows with missing payment details as 'slow-completers'.
    """
    if payment_column not in df.columns:
        found_cols = [c for c in df.columns if 'payment' in c]
        payment_column = found_cols[0] if found_cols else None

    if payment_column:
        df['customer_status'] = df[payment_column].apply(
            lambda x: 'slow-completers' if pd.isna(x) or str(x).strip().lower() in ['none', ''] else 'active'
        )
    else:
        df['customer_status'] = 'unknown'
        print(f"⚠️ Warning: Could not find a payment column to flag statuses.")

    return df