import os
import pandas as pd
import pytest
from train_moodle_model import load_clean_csv  # Corrected: no '.py' extension


def test_load_clean_csv_format():
    """
    Test that our loader cleans quotes and handles semicolons properly
    """
    # 1. Create a temporary semicolon-separated mock CSV file
    test_file = "test_temp.csv"
    with open(test_file, "w") as f:
        f.write('"Header1";"Header2"\n"value1";"value2"\n')

    try:
        # 2. Process with your ETL loader function
        df = load_clean_csv(test_file)

        # 3. Assert schema expectations
        assert "Header1" in df.columns
        assert df["Header1"].iloc[0] == "value1"
        assert '"' not in df["Header1"].iloc[0]

    finally:
        # 4. Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)