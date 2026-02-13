import pandas as pd
import os
from datetime import datetime

DATA_FILE = "attendance_log.csv"
COLUMNS = ["Date", "Start_Time", "End_Time", "Hours", "Rate", "Earnings"]

def load_data():
    """Loads the attendance data from CSV."""
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=COLUMNS)
    try:
        df = pd.read_csv(DATA_FILE)
        # Ensure columns match in case of file corruption or versioning
        if not all(col in df.columns for col in COLUMNS):
             return pd.DataFrame(columns=COLUMNS)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(columns=COLUMNS)

def save_entry(date, start_time, end_time, rate):
    """Calculates hours and earnings, then appends to CSV."""
    try:
        # Calculate hours
        fmt = "%H:%M"
        t1 = datetime.strptime(start_time, fmt)
        t2 = datetime.strptime(end_time, fmt)
        
        # Handle overnight shifts (e.g. 23:00 to 02:00)
        if t2 < t1:
            diff = (t2 - t1).seconds / 3600 + 24
        else:
            diff = (t2 - t1).seconds / 3600
            
        hours = round(diff, 2)
        earnings = round(hours * float(rate), 2)

        new_entry = {
            "Date": date,
            "Start_Time": start_time,
            "End_Time": end_time,
            "Hours": hours,
            "Rate": rate,
            "Earnings": earnings
        }
        
        df = load_data()
        entry_df = pd.DataFrame([new_entry])
        df = pd.concat([df, entry_df], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        return True, "Entry saved successfully!"
    except Exception as e:
        return False, f"Error saving entry: {str(e)}"

def delete_entry(index):
    """Deletes an entry by index."""
    try:
        df = load_data()
        if 0 <= index < len(df):
            df = df.drop(index).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            return True, "Entry deleted."
        return False, "Index out of range."
    except Exception as e:
        return False, f"Error deleting entry: {str(e)}"
