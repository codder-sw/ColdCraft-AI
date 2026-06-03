import pandas as pd
import os

def clean_junk_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Scans the dataframe to locate where the real headers reside,
    removes top-level metadata lines, and resets columns properly.
    """
    target_keywords = {'name', 'job title', 'linkedin url', 'interests', 'skills'}
    header_row_index = None

    # Step 1: Scan rows to find the true column headers
    for idx, row in df.iterrows():
        # Convert row values to lowecase strings to perform safe matching
        row_values = [str(val).strip().lower() for val in row.values]
        
        # Check if any target keyword matches the row items
        if any(keyword in row_values for keyword in target_keywords):
            header_row_index = idx
            break

    # Step 2: If header is found deep in the sheet, realign the dataframe
    if header_row_index is not None and header_row_index > 0:
        # Extract new headers from that specific row
        new_headers = df.iloc[header_row_index].astype(str).str.strip().tolist()
        
        # Slice data from the row below the header onwards
        df = df.iloc[header_row_index + 1 :].copy()
        df.columns = new_headers
        
    # Step 3: Remove completely empty rows or columns that got imported accidentally
    df = df.dropna(how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed:')] # Drop ghost columns
    df = df.reset_index(drop=True)
    
    return df

def load_any_file(file_path: str) -> pd.DataFrame:
    """
    Loads CSV or Excel datasets safely and triggers the cleaning pipeline automatically.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at: {file_path}")

    ext = os.path.splitext(file_path)[-1].lower()

    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported format! Only CSV or Excel sheets are accepted.")

    # Apply our smart cleaning function right after loading the file
    cleaned_df = clean_junk_rows(df)
    return cleaned_df