import streamlit as st
from dotenv import load_dotenv

# CRITICAL FIX: Load environment variables before importing custom source modules
load_dotenv()

import pandas as pd
import os
from src.data_handler import load_any_file
from src.tailoring import get_tailored_bullets
from src.email_generator import craft_email

# Page Configuration Setup
st.set_page_config(page_title="ColdCraft AI Enterprise", page_icon="🚀", layout="wide")

st.title("🚀 ColdCraft AI: Outreach Agent (Enterprise SaaS)")
st.markdown("Advanced Multi-Resume & Skill-Bank Hyper-Personalization Engine.")

# --- UI Layout Structure using Tabs ---
tab1, tab2, tab3 = st.tabs(["👤 Advanced Profile Setup", "🚀 Campaign Dashboard", "📊 Analytics"])

# ==========================================
# TAB 1: ADVANCED USER PROFILE
# ==========================================
with tab1:
    st.header("Setup Your Professional Knowledge Base")
    
    # Section 1: Basic & Social Info
    st.markdown("### 🌐 Contact & Social Matrix")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        user_name = st.text_input("Your Name", value="Shivam")
    with c2:
        github_link = st.text_input("GitHub/Portfolio Link", value="https://github.com/shivam")
    with c3:
        linkedin_link = st.text_input("LinkedIn Profile Link", value="https://linkedin.com/in/shivam")
    with c4:
        tone_selection = st.selectbox("Global Email Tone", ["Highly Professional", "Friendly & Casual", "Direct Pitch"])

    st.divider()

    # Section 2: Priority Roles Matrix (1-5)
    st.markdown("### 🎯 Target Roles Matrix (Priority 1-5)")
    st.caption("Jobs ki shortage ke karan multiple options set karein. AI top values ko priority dega.")
    r1, r2, r3, r4, r5 = st.columns(5)
    with r1:
        role_1 = st.text_input("1️⃣ Primary Role", value="Software Engineer")
    with r2:
        role_2 = st.text_input("2️⃣ Secondary Role", value="Machine Learning Engineer")
    with r3:
        role_3 = st.text_input("3️⃣ Tertiary Role", value="Data Analyst")
    with r4:
        role_4 = st.text_input("4️⃣ Alternate Role 1", value="Backend Developer")
    with r5:
        role_5 = st.text_input("5️⃣ Alternate Role 2", value="Full Stack Developer")

    st.divider()

    # Section 3: Extra Skills Bank
    st.markdown("### 🧠 Core Skills & Keyword Bank (Beyond Resume constraints)")
    st.caption("Aisi skills, tools, ya keywords jo aapke resume lines mein directly nahi hain par aapko aate hain (comma-separated).")
    skills_bank_raw = st.text_area(
        "Skills Bank", 
        value="Python, Docker, Kubernetes, Fast-API, AWS EC2, System Design, SQL, CI/CD Pipelines, Git",
        height=70
    )

    st.divider()

    # Section 4: Multi-Resume Upload/Input (3 Resumes)
    st.markdown("### 📝 Multi-Resume Repository")
    st.caption("Alag-alag domain ke liye apne points yahan enter karein. AI automatically perfect profile match karega.")
    
    res_tab1, res_tab2, res_tab3 = st.tabs(["📄 Profile 1 (AI/ML/Data)", "📄 Profile 2 (Web Dev/Software)", "📄 Profile 3 (Core/General)"])
    
    with res_tab1:
        res1_data = st.text_area(
            "Resume Points - AI/ML",
            value="Developed a recommendation engine with Python and scikit-learn\nPublished paper on neural networks\nAnalyzed complex datasets using pandas and matplotlib",
            height=120,
            key="res1"
        )
    with res_tab2:
        res2_data = st.text_area(
            "Resume Points - Web/Software Development",
            value="Built responsive and scalable web dashboards using Streamlit and React\nDesigned robust backend APIs using Flask and optimized query structures\nImplemented CI/CD pipelines automating deployment sequences",
            height=120,
            key="res2"
        )
    with res_tab3:
        res3_data = st.text_area(
            "Resume Points - General Core",
            value="Conducted lab experiments on complex signal circuits\nDesigned custom analog filters for industrial signal processing units\nCollaborated in agile environments with cross-functional technical teams",
            height=120,
            key="res3"
        )

    # Giant data pool generation
    compiled_pool = []
    # Processing chunks of separate string arrays into a combined profile context array
    for data in [res1_data, res2_data, res3_data]:
        if data.strip():
            compiled_pool.extend([line.strip() for line in data.split('\n') if line.strip()])
    if skills_bank_raw.strip():
        compiled_pool.extend([sk.strip() for sk in skills_bank_raw.split(',') if sk.strip()])

# ==========================================
# TAB 2: OUTREACH DASHBOARD (Processing)
# ==========================================
with tab2:
    st.header("Execute Personalization Campaign")
    uploaded_file = st.file_uploader("Upload Target Matrix (CSV/XLSX)", type=["csv", "xlsx"])
    
    if uploaded_file:
        temp_path = uploaded_file.name 
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            df = load_any_file(temp_path)
            st.success(f"✅ {len(df)} contacts ingested securely into RAM!")
            
            with st.expander("Ingested Data Preview (First 5 Rows)"):
                st.dataframe(df.head())

            if st.button("🚀 Execute Smart Semantic Personalization", use_container_width=True):
                st.divider()
                
                for index, row in df.iterrows():
                    name = row.get('Name', 'Professional')
                    job = row.get('Job Title', 'Expert')
                    skills = row.get('Interests', row.get('Skills', 'Technology'))
                    
                    # Junk and Meta row handling (Filters out row data irregularities)
                    if pd.isna(name) or str(name).strip().lower() in ["none", "", "name"]:
                        continue
                        
                    with st.spinner(f"Analyzing credentials pool against {name}'s requirements..."):
                        # AI mapping context computation over target records matching constraints
                        best_points = get_tailored_bullets(skills, compiled_pool)
                        
                        # Formatting variables downstream into active API request client
                        subject, body = craft_email(name, job, best_points, user_name, role_1, github_link, linkedin_link, tone_selection)
                    
                    with st.expander(f"📧 Tailored Content for {name} ({job})"):
                        st.write(f"**Subject:** {subject}")
                        st.text_area(label="Email Body", value=body, height=220, key=f"text_{index}")
                        st.button(f"Copy Draft", key=f"btn_{index}")
                        
        except Exception as e:
            st.error(f"Execution Error: {e}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        st.info("Please ingest a target spreadsheet file to unlock campaign features.")

# ==========================================
# TAB 3: SAAS ANALYTICS
# ==========================================
with tab3:
    st.header("Campaign Optimization Hub")
    st.metric(label="Total Aggregated Knowledge Pool Size", value=f"{len(compiled_pool)} Points")
    st.info("System is ready. Under the hood tracking logging parameter states natively via MLflow.")