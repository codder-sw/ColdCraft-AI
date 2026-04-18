from sentence_transformers import SentenceTransformer, util
import torch

# 1. AI Model load karna
# Hum 'all-mpnet-base-v2' use kar rahe hain jo ki high-quality vectors banata hai [cite: 92]
print("AI Model load ho raha hai... Thoda intezar karein.")
model = SentenceTransformer('all-mpnet-base-v2') 

def find_best_matches(job_description, resume_points):
    # 2. Text ko math (vectors) mein badalna
    # Is process ko 'Encoding' kehte hain [cite: 104]
    job_vec = model.encode(job_description, convert_to_tensor=True)
    resume_vecs = model.encode(resume_points, convert_to_tensor=True)

    # 3. Similarity Score nikalna (Cosine Similarity)
    # Ye 0 se 1 ke beech batata hai ki kitna match hai [cite: 107]
    cosine_scores = util.cos_sim(job_vec, resume_vecs)[0]

    # 4. Top 2 matching points nikalna
    top_results = torch.topk(cosine_scores, k=2)
    
    print(f"\nTarget Job: {job_description}")
    print("-" * 30)
    print("Top Matching Resume Points (AI ke hisaab se):")
    
    for score, idx in zip(top_results.values, top_results.indices):
        # Score ko percentage mein dikhane ke liye 100 se multiply kiya
        match_pct = score.item() * 100
        print(f"- {resume_points[idx]} (Match Score: {match_pct:.2f}%)")

if __name__ == "__main__":
    # Test Data: Sochiye aapka resume aur ek job description
    job = "Looking for someone who knows Machine Learning and Python"
    
    my_resume_points = [
        "Built a neural network using Python",
        "Expert in circuit design and hardware",
        "Data analysis using pandas library",
        "Good at playing football"
    ]
    
    find_best_matches(job, my_resume_points)