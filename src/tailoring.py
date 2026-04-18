import pandas as pd
from semantic_match import model # Jo model aapne download kiya, wahi use karenge [cite: 92]
from sentence_transformers import util

def get_tailored_bullets(target_skills, resume_bullets):
    # 1. Target skills aur resume points ko math (vectors) mein badalna [cite: 101]
    target_vec = model.encode(target_skills, convert_to_tensor=True)
    bullet_vecs = model.encode(resume_bullets, convert_to_tensor=True)

    # 2. Similarity score nikalna [cite: 106]
    cosine_scores = util.cos_sim(target_vec, bullet_vecs)[0]

    # 3. Bullets ko score ke hisaab se sort (arrange) karna [cite: 65, 83]
    scored_bullets = []
    for i in range(len(resume_bullets)):
        scored_bullets.append({
            "text": resume_bullets[i],
            "score": cosine_scores[i].item()
        })
    
    # Sabse zyada score wale top 3 points nikalna [cite: 66, 83]
    sorted_bullets = sorted(scored_bullets, key=lambda x: x['score'], reverse=True)
    return [b['text'] for b in sorted_bullets[:3]]

def run_tailoring():
    # Aapka asli/base resume [cite: 21, 233]
    my_base_resume = [
        "Developed a recommendation engine with Python and scikit-learn",
        "Conducted lab experiments on signal circuits",
        "Published paper on neural networks",
        "Analyzed datasets using pandas and matplotlib",
        "Designed analog filters for signal processing"
    ]

    try:
        # Step 1: Processed data load karna [cite: 12]
        df = pd.read_csv('data/processed_recipients.csv')
        
        print("\n--- Tailoring Resumes for Each Recipient ---")
        
        for index, row in df.iterrows():
            # Har insaan ke liye best points nikalna 
            top_points = get_tailored_bullets(row['Inferred_Skills'], my_base_resume)
            
            print(f"\nRecipient: {row['Name']} ({row['Job Title']})")
            print(f"Target Skills: {row['Inferred_Skills']}")
            print("Tailored Resume Bullets:")
            for p in top_points:
                print(f"  -> {p}")
                
    except FileNotFoundError:
        print("Error: 'data/processed_recipients.csv' nahi mili. Pehle profile_extraction.py chalayein.")

if __name__ == "__main__":
    run_tailoring()