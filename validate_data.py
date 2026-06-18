import os
import pandas as pd

EXCEL_FILE = "Copy of Task 1 Dataset.xlsx"


def validate_dataset():
    print("Starting data validation checks...")

    # Check file existence
    if not os.path.exists(EXCEL_FILE):
        print(f"Error: {EXCEL_FILE} does not exist!")
        exit(1)

    df = pd.read_excel(EXCEL_FILE)

    # Check rows and columns shape
    expected_rows = 900
    expected_cols = 18
    actual_rows, actual_cols = df.shape

    assert (
        actual_rows == expected_rows
    ), f"Row count mismatch! Expected {expected_rows}, got {actual_rows}"
    assert (
        actual_cols == expected_cols
    ), f"Column count mismatch! Expected {expected_cols}, got {actual_cols}"
    print(f"[OK] Shape Check: ({actual_rows} rows, {actual_cols} columns)")

    # Check required columns
    required_cols = [
        "Accuracy Rate",
        "Response Rate",
        "Error Rate",
        "Persistence Rate",
        "Consistency Rate",
        "Overall Performance Score",
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column: {col}"
        # Check for NaNs
        nan_count = df[col].isna().sum()
        assert nan_count == 0, f"Column '{col}' has {nan_count} missing (NaN) values!"
        # Check range [0, 100]
        min_val = df[col].min()
        max_val = df[col].max()
        assert (
            0.0 <= min_val <= 100.0
        ), f"Column '{col}' min value {min_val} is out of [0, 100] bound!"
        assert (
            0.0 <= max_val <= 100.0
        ), f"Column '{col}' max value {max_val} is out of [0, 100] bound!"
        print(f"[OK] Column '{col}': No NaNs, values in range [{min_val:.2f}, {max_val:.2f}]")

    print("\n[SUCCESS] Automated Validation: SUCCESSFUL! All checks passed.")


if __name__ == "__main__":
    validate_dataset()
