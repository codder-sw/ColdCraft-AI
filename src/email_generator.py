def craft_email(name, job_title, matched_bullets):
    """
    Ye function recipient ke liye ek personalized email draft taiyar karta hai.
    """
    # Subject Line humesha relevant honi chahiye [cite: 144]
    subject = f"Connecting regarding {job_title} opportunities - {name}"
    
    # Body mein hum wahi points use karte hain jo AI ne match kiye hain [cite: 116]
    body = (
        f"Dear {name},\n\n"
        f"I am reaching out because of your impressive work as a {job_title}. "
        f"Based on my background, I have experience in {', '.join(matched_bullets)}, "
        f"which aligns closely with the skills you value.\n\n"
        "I would appreciate a brief 10-minute chat to discuss how I could contribute to your team.\n\n"
        "Best regards,\n[Your Name]"
    )
    
    return subject, body