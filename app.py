import streamlit as st
from utils.file_utils import handle_file_upload
from assistant.workflow_builder import build_workflow
from assistant.email_generator import generate_cover_letter_and_email

# Configure the page
st.set_page_config(page_title="AI Resume Assistant", layout="wide")

# Custom CSS for advanced styling, including fonts, animations, and colors
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
    /* Global styles and gradient background */
    body {
        background: linear-gradient(135deg, #DCE35B 0%, #45B649 100%);
        font-family: 'Montserrat', sans-serif;
        color: #2c3e50;
    }
    /* Title styling */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 30px;
        color: #2c3e50;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        animation: fadeInDown 1s ease;
    }
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        border-bottom: 3px solid #27ae60;
        padding-bottom: 10px;
        margin-top: 40px;
        margin-bottom: 20px;
        animation: fadeInLeft 0.7s ease;
    }
    /* Content boxes */
    .content-box {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        animation: fadeInUp 0.8s ease;
    }
    /* Labels for uploaders */
    .upload-label {
        font-size: 1.2rem;
        font-weight: 500;
        color: #1abc9c;
    }
    /* Animate text areas so they fade in smoothly */
    .stTextArea textarea {
        animation: fadeInUp 1s ease;
        background-color: #ffffff !important;
        color: #2c3e50 !important;
    }
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
    }
    /* Keyframes for animations */
    @keyframes fadeInDown {
      0% {
        opacity: 0;
        transform: translateY(-20px);
      }
      100% {
        opacity: 1;
        transform: translateY(0);
      }
    }
    @keyframes fadeInLeft {
      0% {
        opacity: 0;
        transform: translateX(-20px);
      }
      100% {
        opacity: 1;
        transform: translateX(0);
      }
    }
    @keyframes fadeInUp {
      0% {
        opacity: 0;
        transform: translateY(20px);
      }
      100% {
        opacity: 1;
        transform: translateY(0);
      }
    }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.markdown("<div class='main-title'>AI Resume Assistant</div>", unsafe_allow_html=True)

# Sidebar for instructions and feedback
st.sidebar.markdown("<div class='section-header'>Instructions</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
1. Upload your resume and job description below.
2. Review the extracted text in the main area.
3. Our AI Assistant will generate an ATS-friendly resume, cover letter, and cold email.
4. Provide feedback in the sidebar to refine the resume further.
""")

# Upload section
st.markdown("<div class='section-header'>Upload Your Documents</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("<span class='upload-label'>Upload Resume</span>", unsafe_allow_html=True)
    resume_file = st.file_uploader("", type=["txt", "pdf", "docx"], key="resume_uploader")
with col2:
    st.markdown("<span class='upload-label'>Upload Job Description</span>", unsafe_allow_html=True)
    job_desc_file = st.file_uploader("", type=["txt", "pdf", "docx"], key="job_desc_uploader")

if resume_file and job_desc_file:
    try:
        # Convert the files to text
        resume_text = handle_file_upload(resume_file)
        job_desc_text = handle_file_upload(job_desc_file)

        # Display original content in columns
        st.markdown("<div class='section-header'>Original Document Content</div>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("<div class='content-box'><strong>Resume Content:</strong></div>", unsafe_allow_html=True)
            st.text_area("", resume_text, height=300, key="orig_resume")
        with col4:
            st.markdown("<div class='content-box'><strong>Job Description Content:</strong></div>", unsafe_allow_html=True)
            st.text_area("", job_desc_text, height=300, key="orig_job_desc")

        # Build the workflow and invoke it
        st.markdown("<div class='section-header'>Processing Documents...</div>", unsafe_allow_html=True)
        graph = build_workflow()
        initial_state = {
            "resume": resume_text,
            "job_desc": job_desc_text,
            "updated_resume": "",
            "feedback": "",
            "evaluation": ""
        }
        st.write("**Initial State:**", initial_state)
        final_state = graph.invoke(initial_state)
        st.write("**Final State:**", final_state)

        # Display ATS-friendly resume
        st.markdown("<div class='section-header'>ATS-Friendly Resume</div>", unsafe_allow_html=True)
        st.text_area("", final_state.get("updated_resume", "No updated resume available"), height=300, key="ats_resume")

        # Generate cover letter and cold email
        st.markdown("<div class='section-header'>Cover Letter & Cold Email</div>", unsafe_allow_html=True)
        generated_content = generate_cover_letter_and_email(final_state.get("updated_resume", ""), job_desc_text)
        st.markdown("<div class='content-box'><strong>Cover Letter:</strong></div>", unsafe_allow_html=True)
        st.text_area("", generated_content['cover_letter'], height=300, key="cover_letter")
        st.markdown("<div class='content-box'><strong>Cold Email:</strong></div>", unsafe_allow_html=True)
        st.text_area("", generated_content['cold_email'], height=300, key="cold_email")

        # Feedback section in the sidebar
        st.sidebar.markdown("<div class='section-header'>Feedback</div>", unsafe_allow_html=True)
        feedback = st.sidebar.text_input("Provide Feedback on Resume (if needed):")
        if feedback:
            initial_state["feedback"] = feedback
            final_state = graph.invoke(initial_state)
            st.markdown("<div class='section-header'>Updated ATS-Friendly Resume (After Feedback)</div>", unsafe_allow_html=True)
            st.text_area("", final_state["updated_resume"], height=300, key="updated_resume_feedback")

    except Exception as e:
        st.error(f"Error: {e}")
