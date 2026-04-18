import streamlit as st
import pandas as pd
import os
from src.data_handler import load_any_file
from src.tailoring import get_tailored_bullets
from src.email_generator import craft_email

# Page Setup
st.set_page_config(page_title="ColdCraft AI", page_icon="🚀", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 ColdCraft AI: Outreach Agent")
st.info("AI-powered system jo aapke resume ko target role ke hisaab se tailor karta hai.")

# 1. File Upload Section
with st.sidebar:
    st.header("Settings")
    uploaded_file = st.file_uploader("Upload Contacts (CSV/XLSX/PDF)", type=["csv", "xlsx", "pdf"])
    st.divider()
    st.write("Made for Students 🎓")

if uploaded_file:
    # Temporary file save karna taaki data_handler read kar sake
    temp_path = "temp_upload_file"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        df = load_any_file(temp_path)
        st.success(f"✅ {len(df)} contacts successfully load ho gaye!")
        
        # Data Preview
        with st.expander("Data Preview (Pehli 5 rows)"):
            st.dataframe(df.head())

        # Base Resume Content
        base_resume = [
            "Developed a recommendation engine with Python and scikit-learn",
            "Conducted lab experiments on signal circuits",
            "Published paper on neural networks",
            "Analyzed datasets using pandas and matplotlib"
        ]

        if st.button("Generate Personalized Emails ✨"):
            st.divider()
            cols = st.columns(1) # Layout fix
            
            for index, row in df.iterrows():
                # Column names check (Safe handling)
                name = row.get('Name', 'Professional')
                job = row.get('Job Title', 'Expert')
                skills = row.get('Interests', row.get('Skills', 'Technology'))
                
                # AI Matching Logic
                with st.spinner(f"Matching resume for {name}..."):
                    best_points = get_tailored_bullets(skills, base_resume)
                    subject, body = craft_email(name, job, best_points)
                
                # Result Display
                with st.expander(f"📧 Email Draft for {name} ({job})"):
                    st.write(f"**Subject:** {subject}")
                    st.text_area(label="Draft Content", value=body, height=250, key=f"text_{index}")
                    st.button(f"Copy Content for {name}", key=f"btn_{index}")

    except Exception as e:
        st.error(f"Galti Hui: {e}")
    finally:
        # Cleanup: temp file delete karna zaruri hai
        if os.path.exists(temp_path):
            os.remove(temp_path)
else:
    st.warning("Shuru karne ke liye upar di gayi file upload karein.")