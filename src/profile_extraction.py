import pandas as pd

def extract_skills(title):
    # Title se skills pehchanne ka logic
    skills = []
    title = str(title).lower()
    if "data" in title or "machine learning" in title:
        skills.append("Data Science")
    if "hr" in title or "manager" in title:
        skills.append("Hiring")
    return ", ".join(skills) if skills else "General Outreach"

def run_extraction():
    try:
        # 1. Data load karo (Extract)
        df = pd.read_csv('data/recipients.csv')
        
        # 2. Skills pehchano (Transform)
        df['Inferred_Skills'] = df['Job Title'].apply(extract_skills)
        
        # 3. Terminal pe result dikhao
        print("\n--- Processed Data ---")
        print(df[['Name', 'Inferred_Skills']])
        
        # 4. Result save karo (Load)
        df.to_csv('data/processed_recipients.csv', index=False)
        print("\nSuccess! Nayi file 'data/processed_recipients.csv' ban gayi hai.")
        
    except Exception as e:
        print(f"Kuch galti hui: {e}")

if __name__ == "__main__":
    run_extraction()