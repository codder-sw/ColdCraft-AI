import pandas as pd
from sentence_transformers import util
import os

# 1. YAHAN CHANGE HAI: Streamlit aur Pipeline dono ke liye path fix kiya
try:
    # Jab app.py se chale (Web UI)
    from src.semantic_match import model
except ImportError:
    # Jab direct src/ folder se chale (Terminal)
    from semantic_match import model

def get_tailored_bullets(target_skills, resume_bullets):
    # 1. Target skills aur resume points ko math (vectors) mein badalna
    target_vec = model.encode(target_skills, convert_to_tensor=True)
    bullet_vecs = model.encode(resume_bullets, convert_to_tensor=True)

    # 2. Similarity score nikalna (Cosine Similarity)
    cosine_scores = util.cos_sim(target_vec, bullet_vecs)[0]

    # 3. Bullets ko score ke hisaab se sort karna
    scored_bullets = []
    for i in range(len(resume_bullets)):
        scored_bullets.append({
            "text": resume_bullets[i],
            "score": cosine_scores[i].item()
        })
    
    # Sabse zyada score wale top 3 points nikalna
    sorted_bullets = sorted(scored_bullets, key=lambda x: x['score'], reverse=True)
    return [b['text'] for b in sorted_bullets[:3]]

def run_tailoring():
    # Aapka asli resume content
    my_base_resume = [
        "Developed a recommendation engine with Python and scikit-learn",
        "Conducted lab experiments on signal circuits",
        "Published paper on neural networks",
        "Analyzed datasets using pandas and matplotlib",
        "Designed analog filters for signal processing"
    ]

    # File path fix (taaki folder ke bahar se bhi chale)
    data_path = 'data/processed_recipients.csv'
    if not os.path.exists(data_path):
        data_path = '../data/processed_recipients.csv'

    try:
        df = pd.read_csv(data_path)
        print("\n--- Tailoring Resumes for Each Recipient ---")
        
        for index, row in df.iterrows():
            top_points = get_tailored_bullets(row['Inferred_Skills'], my_base_resume)
            print(f"\nRecipient: {row['Name']} ({row['Job Title']})")
            print(f"Target Skills: {row['Inferred_Skills']}")
            print("Tailored Resume Bullets:")
            for p in top_points:
                print(f"  -> {p}")
                
    except Exception as e:
        print(f"Error: Data load nahi ho paya. Details: {e}")

if __name__ == "__main__":
    run_tailoring()