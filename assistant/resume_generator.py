from langchain.chat_models import ChatOpenAI
import os

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)


def generate_ats_friendly_resume(resume_text: str, job_desc_text: str) -> str:
    """
    Generates an ATS-friendly resume by updating the original resume with relevant keywords from the job description.
    The output should be well-formatted with clear section headers and appropriate spacing.
    """
    prompt = f"""
    You are a professional resume editor. Given the following original resume and job description, update the resume to be more ATS-friendly.
    
    Tasks:
    1. Reformat the resume so that each section (Contact Information, Education, Skills, Projects, Work Experience) is clearly separated with headers.
    2. Incorporate relevant keywords from the job description (e.g., "NLP", "Machine Learning", "Data Engineering") naturally into the resume.
    3. Ensure the resume is clearly spaced and easy to read.
    
    Original Resume:
    {resume_text}
    
    Job Description:
    {job_desc_text}
    
    Please provide the updated, well-formatted resume.
    """
    response = llm.invoke(prompt)
    return response.content