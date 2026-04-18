import pandas as pd
import pdfplumber
import os

def load_any_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Bhai, ye file nahi mili: {file_path}")

    ext = os.path.splitext(file_path)[-1].lower()
    
    # 1. Excel handling
    if ext in ['.xlsx', '.xls']:
        print(f"📂 Excel file mil gayi: {file_path}")
        return pd.read_excel(file_path)
    
    # 2. CSV handling
    elif ext == '.csv':
        return pd.read_csv(file_path)
    
    # 3. PDF handling
    elif ext == '.pdf':
        print(f"📄 PDF detect hui. Tables nikal raha hoon...")
        all_data = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_data.append(df)
        if not all_data:
            print("⚠️ PDF mein koi table nahi mili!")
            return pd.DataFrame()
        return pd.concat(all_data, ignore_index=True)
    
    else:
        print(f"❌ '{ext}' format abhi supported nahi hai.")
        return pd.DataFrame()

if __name__ == "__main__":
    # Test karne ke liye (Optional):
    # df = load_any_file('data/recipients.csv')
    # print(df.head())
    pass