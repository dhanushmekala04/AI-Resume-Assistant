from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import ChatOpenAI
from assistant.resume_generator import generate_ats_friendly_resume as ats_resume_func
from assistant.job_description_analyzer import analyze_job_description
from assistant.email_generator import generate_cover_letter_and_email

# Initialize the LLM (using ChatOpenAI from LangChain)
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)


# Define the state for the workflow
class State(TypedDict):
    resume: str
    job_desc: str
    updated_resume: str
    feedback: str
    evaluation: str

def analyze_resume_and_job_desc(state: State) -> State:
    """
    Pass through the state. (In a real application, you might extract key info here.)
    """
    new_state = state.copy()
    return new_state

def node_generate_ats_friendly_resume(state: State) -> State:
    """
    Generate an ATS-friendly resume by calling the resume generator function.
    """
    updated = ats_resume_func(state["resume"], state["job_desc"])
    new_state = state.copy()
    new_state["updated_resume"] = updated
    return new_state

def evaluate_content(state: State) -> State:
    """
    Evaluate the generated resume for quality.
    Here, we simulate evaluation by marking it as accepted.
    """
    evaluation = "accepted"  # Change to "needs improvement" to test feedback
    feedback = "Looks good!"  # Sample feedback; in real cases, use LLM evaluation
    new_state = state.copy()
    new_state["evaluation"] = evaluation
    new_state["feedback"] = feedback
    return new_state

def user_feedback_loop(state: State) -> State:
    """
    Handle feedback for improving the generated resume.
    """
    new_state = state.copy()
    if state["evaluation"] == "needs improvement" and state["feedback"]:
        updated_resume = f"{state['updated_resume']} - Based on feedback: {state['feedback']}"
        new_state["updated_resume"] = updated_resume
        new_state["evaluation"] = "accepted"
    return new_state

def route_output(state: State) -> str:
    """
    Decide whether to accept the output or loop back for improvement.
    """
    if state["evaluation"] == "accepted":
        return "Accepted"
    else:
        return "Rejected + Feedback"

def build_workflow():
    """
    Build and return the LangGraph workflow for the job application assistant.
    """
    builder = StateGraph(State)
    
    builder.add_node("analyze_resume_and_job_desc", analyze_resume_and_job_desc)
    builder.add_node("generate_ats_friendly_resume", node_generate_ats_friendly_resume)
    builder.add_node("evaluate_content", evaluate_content)
    builder.add_node("user_feedback_loop", user_feedback_loop)
    
    builder.add_edge(START, "analyze_resume_and_job_desc")
    builder.add_edge("analyze_resume_and_job_desc", "generate_ats_friendly_resume")
    builder.add_edge("generate_ats_friendly_resume", "evaluate_content")
    builder.add_edge("evaluate_content", "user_feedback_loop")
    
    builder.add_conditional_edges(
        "user_feedback_loop",
        route_output,
        {"Accepted": END, "Rejected + Feedback": "generate_ats_friendly_resume"}
    )
    
    return builder.compile()
