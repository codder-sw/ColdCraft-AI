import pandas as pd
import mlflow  # Experiment tracking ke liye
import time
import os
from data_handler import load_any_file  # Naya Data Handler import
from tailoring import get_tailored_bullets
from email_generator import craft_email

# Experiment ka naam set karein
mlflow.set_experiment("ColdCraft_Outreach_v1")

def start_automation():
    # 1. File Path set karein (Yahan aap recipients.xlsx ya recipients.pdf bhi likh sakte hain)
    input_file = 'data/recipients.csv' 
    
    print(f"🚀 ColdCraft AI: Outreach Pipeline Shuru Ho Rahi Hai...")
    print(f"📂 Processing File: {input_file}\n")

    # MLflow Tracking shuru
    with mlflow.start_run():
        mlflow.log_param("input_file", input_file)
        mlflow.log_param("model_type", "SBERT-Semantic-Match")

        # Aapka main resume content
        base_resume = [
            "Developed a recommendation engine with Python and scikit-learn",
            "Conducted lab experiments on signal circuits",
            "Published paper on neural networks",
            "Analyzed datasets using pandas and matplotlib"
        ]

        try:
            # 2. Smart Loading: CSV, Excel ya PDF apne aap detect hogi
            df = load_any_file(input_file)
            
            if df.empty:
                print("⚠️ Bhai, file khali hai ya data nahi mila!")
                return

            mlflow.log_metric("total_recipients", len(df))

            for index, row in df.iterrows():
                # Safety check: Agar Name ya Job Title missing ho
                name = row.get('Name', 'Professional')
                job_title = row.get('Job Title', 'Expert')
                skills = row.get('Interests', 'Technology') # Interests ko skills ki tarah use kar rahe hain

                print(f"--- Processing: {name} ({job_title}) ---")
                
                # 3. Semantic Match
                best_points = get_tailored_bullets(skills, base_resume)
                
                # 4. Email Draft
                subject, body = craft_email(name, job_title, best_points)
                
                print(f"✅ Email Draft Ready!")
                print(f"Subject: {subject}\n")
                
                # Rate Limiting for Deliverability
                time.sleep(1) 
                
            print("🎉 Mission Accomplished! Saare drafts taiyar hain aur MLflow mein tracked hain.")

        except Exception as e:
            mlflow.log_param("error_log", str(e))
            print(f"❌ Galti Hui: {e}")

if __name__ == "__main__":
    start_automation()