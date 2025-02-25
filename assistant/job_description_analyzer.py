def analyze_job_description(job_desc: str) -> dict:
    """
    Extracts key skills and qualifications from the job description.
    For simplicity, returns sample keywords.
    """
    job_skills = ["Python", "Machine Learning", "NLP", "Data Analysis", "Deep Learning"]
    return {"required_skills": job_skills, "job_description": job_desc}
