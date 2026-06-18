import pandas as pd
from app.calculator import (
    calculate_accuracy_rate,
    calculate_response_rate,
    calculate_error_rate,
    calculate_persistence_rate,
    calculate_consistency_rate,
    calculate_overall_performance_score,
)

EXCEL_FILE = "Copy of Task 1 Dataset.xlsx"


def process_dataset():
    print(f"Reading dataset: {EXCEL_FILE}")
    df = pd.read_excel(EXCEL_FILE)

    print("Computing derived rates...")
    for idx, row in df.iterrows():
        # Extracted metrics
        dur = int(row["session_duration_seconds"])
        sliced = int(row["fruits_sliced"])
        missed = int(row["fruits_missed"])
        hit = int(row["bombs_hit"])
        dodged = int(row["bombs_dodged"])
        combo = int(row["max_combo"])
        pauses = int(row["pause_count"])
        retries = int(row["retries"])

        # Calculated rates
        acc = calculate_accuracy_rate(sliced, missed, hit)
        resp = calculate_response_rate(sliced, dodged, combo, dur)
        err = calculate_error_rate(sliced, missed, hit, dodged)
        pers = calculate_persistence_rate(retries, dur, pauses)
        cons = calculate_consistency_rate(combo, sliced, err, pauses)
        overall = calculate_overall_performance_score(acc, resp, err, pers, cons)

        # Update in dataframe
        df.at[idx, "Accuracy Rate"] = acc
        df.at[idx, "Response Rate"] = resp
        df.at[idx, "Error Rate"] = err
        df.at[idx, "Persistence Rate"] = pers
        df.at[idx, "Consistency Rate"] = cons
        df.at[idx, "Overall Performance Score"] = overall

    print(f"Saving changes to {EXCEL_FILE}...")
    # Using openpyxl to overwrite
    df.to_excel(EXCEL_FILE, index=False)
    print("Excel dataset successfully updated!")

    # Display some stats
    print("\nSummary Statistics of Calculated Columns:")
    calc_cols = [
        "Accuracy Rate",
        "Response Rate",
        "Error Rate",
        "Persistence Rate",
        "Consistency Rate",
        "Overall Performance Score",
    ]
    pd.set_option("display.max_columns", 10)
    pd.set_option("display.width", 1000)
    print(df[calc_cols].describe())


if __name__ == "__main__":
    process_dataset()
