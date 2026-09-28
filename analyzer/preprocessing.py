import pandas as pd

def load_and_validate_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        return None, f"Error reading file: {str(e)}"
    
    required_columns = ['run_id', 'test_name', 'status', 'timestamp', 'environment', 'duration']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        return None, f"Missing required columns: {', '.join(missing)}"
    
    df['status'] = df['status'].str.upper().str.strip()
    invalid_status = df[~df['status'].isin(['PASS', 'FAIL'])]
    if not invalid_status.empty:
        return None, "Invalid status values found. Must be strictly 'PASS' or 'FAIL'."
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    if df['timestamp'].isnull().any():
        return None, "Invalid timestamp format detected."
        
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce').fillna(0.0)
    df = df.sort_values(by=['test_name', 'timestamp'])
    return df, None