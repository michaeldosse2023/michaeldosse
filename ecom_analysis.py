import pandas as pd

def generate_ecom_snapshot(df):
    """Prints a quick intelligence executive summary to the terminal."""
    total_customers = len(df)

    if 'customer_status' in df.columns:
        status_counts = df['customer_status'].value_counts()
        slow_count = status_counts.get('slow-completers', 0)
        slow_percentage = (slow_count / total_customers) * 100 if total_customers > 0 else 0

        print("\n" + "=" * 40)
        print("📊 ECOMMERCE CUSTOMER INTELLIGENCE SNAPSHOT")
        print("=" * 40)
        print(f"Total Transactions Analyzed : {total_customers}")
        print(f"Active Accounts             : {status_counts.get('active', 0)}")
        print(f"Slow-Completers (No Payment): {slow_count} ({slow_percentage:.1f}%)")
        print("=" * 40 + "\n")