from langchain.chat_models import ChatOpenAI
import os

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)


def generate_cover_letter_and_email(resume: str, job_desc: str) -> dict:
    """
    Generates a cover letter and a cold email for the given resume and job description.
    The output is formatted clearly.
    """
    prompt = f"""
    Write a cover letter and a cold email for the following job description.

    Job Description:
    {job_desc}

    Using this resume:
    {resume}

    Format the output as follows:

    COVER_LETTER:
    [Your cover letter text]

    ---

    COLD_EMAIL:
    [Your cold email text]
    """
    response = llm.invoke(prompt)
    parts = response.content.split('---')
    cover_letter = parts[0].replace("COVER_LETTER:", "").strip()
    cold_email = parts[1].replace("COLD_EMAIL:", "").strip() if len(parts) > 1 else ""
    return {"cover_letter": cover_letter, "cold_email": cold_email}