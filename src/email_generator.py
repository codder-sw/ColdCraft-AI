import os
from openai import OpenAI

def craft_email(recipient_name, job_title, matched_bullets, sender_name, sender_role, github_link, linkedin_link, tone):
    """
    Uses Google Gemini (via OpenAI wrapper) to dynamically generate human-like cold emails.
    Safely handles missing API keys without crashing the core system layout.
    """
    
    # Step 1: Check if API key exists inside system RAM
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Links formatting block
    links_formatting = ""
    if github_link: links_formatting += f"- GitHub: {github_link}\n"
    if linkedin_link: links_formatting += f"- LinkedIn: {linkedin_link}\n"

    # 🛡️ SAFE GUARD: If key is missing, return fallback template instantly instead of crashing
    if not api_key or api_key.strip() == "":
        fallback_subject = f"Connecting regarding {job_title} opportunities - {sender_name}"
        fallback_body = (
            f"Hi {recipient_name},\n\n"
            f"I am reaching out regarding the {job_title} track. Based on my background, "
            f"I have extensive experience working with {', '.join(matched_bullets)}, which aligns with your team's focus.\n\n"
            f"Connect with me or view my work here:\n{links_formatting}\n"
            f"Would love to briefly connect for a 10-minute chat.\n\n"
            f"Best,\n{sender_name}"
        )
        return fallback_subject, fallback_body

    # Step 2: Initialize client safely inside the execution flow only when key exists
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    system_prompt = (
        "You are an expert career coach and elite sales copywriter. Your job is to write a compelling, "
        "highly targeted cold outreach email that gets a response. Never sound like a generic AI bot."
    )
    
    user_prompt = f"""
    Write a short, high-converting cold email based on these exact details:
    
    - Sender Name: {sender_name}
    - Sender Current Role: {sender_role}
    - Recipient Name: {recipient_name}
    - Recipient Job Title: {job_title}
    - My Core Matching Skills/Projects: {', '.join(matched_bullets)}
    - Links to include in the signature:
    {links_formatting}
    - Desired Email Tone: {tone}
    
    CRITICAL INSTRUCTIONS:
    1. Keep the email under 120-150 words. Be respectful of their time.
    2. The email body must seamlessly weave in the 'Core Matching Skills/Projects' naturally based on the '{tone}' tone requested. Do not just list them as boring bullet points.
    3. Conclude with a crisp call-to-action asking for a brief 10-minute chat.
    4. Return the output in this EXACT format without any conversational filler before or after:
    SUBJECT: [Write a catchy, relevant subject line here]
    BODY:
    [Write the email body here]
    """

    try:
        # Calling Google Gemini Model securely
        response = client.chat.completions.create(
            model="gemini-1.5-flash", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        full_text = response.choices[0].message.content.strip()
        
        # Parsing Subject and Body
        if "SUBJECT:" in full_text and "BODY:" in full_text:
            subject_part = full_text.split("BODY:")[0].replace("SUBJECT:", "").strip()
            body_part = full_text.split("BODY:")[1].strip()
            return subject_part, body_part
        else:
            return f"Connecting regarding {job_title} role", full_text

    except Exception as e:
        # Fallback dynamic template if API rate limit hits or network fails
        fallback_subject = f"Connecting regarding {job_title} opportunities - {sender_name}"
        fallback_body = f"Hi {recipient_name},\n\nI am reaching out regarding the {job_title} track. I have extensive experience in {', '.join(matched_bullets)}. Would love to briefly connect.\n\nBest,\n{sender_name}"
        return fallback_subject, fallback_body