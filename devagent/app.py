import streamlit as st
import os
from src.devagent.crew import Devagent
from src.devagent.helper import clone_repo, get_vector_db

# --- Page Config ---
st.set_page_config(page_title="Industry Code Analyzer", layout="wide")
st.title("🕵️‍♂️ Multi-Agent Codebase Analyzer")
st.markdown("Analyze repositories and find bugs using a collaborative AI crew.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Settings")
    repo_url = st.text_input("GitHub Repository URL", "https://github.com/Ahmed2797/Travel-Planner-Agent.git")
    user_question = st.text_area("What do you want to know?", "Where is the route optimization logic?")
    analyze_button = st.button("Run Analysis", type="primary")

# --- Resource Caching ---
@st.cache_resource
def initialize_system(repo_url):
    """Clones repo and loads/builds Vector DB once."""
    st.info("🔄 Initializing System (Cloning & Indexing)...")
    repo_path = clone_repo(repo_url)
    vector_db = get_vector_db(index_path="faiss_code_index") 
    return vector_db

# --- Execution Logic ---
if analyze_button:
    try:
        # 1. Setup Retrieval
        vector_db = initialize_system(repo_url)
        # Note: Your search_codebase tool in main.py/tools.py 
        # needs to be accessible to the Crew.
        
        # 2. Kickoff Crew
        with st.status("🚀 Crew is working...", expanded=True) as status:
            st.write("Agents are communicating...")
            crew_system = Devagent()
            crew = crew_system.crew()
            
            result = crew.kickoff(
                inputs={"user_question": user_question}
            )
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        # 3. Display Results
        st.subheader("📋 Analysis Report")
        st.markdown(result)
        
        # Optional: Download button for the report
        st.download_button(
            label="Download Report as Markdown",
            data=str(result),
            file_name="code_analysis_report.md",
            mime="text/markdown"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Enter a repository URL and click 'Run Analysis' to begin.")

## streamlit run app.py