
from crewai.tools import tool
from src.devagent.helper import clone_repo, build_vector_db,get_vector_db




repo = 'https://github.com/Ahmed2797/Travel-Planner-Agent.git'


repo_path = clone_repo(repo)

vector_db = build_vector_db(repo_path)
vector_db = get_vector_db()  # This will load the existing index if it exists, or create a new one if it doesn't
retriever = vector_db.as_retriever()


@tool
def search_codebase(question: str):
    """Searches the repository for relevant code snippets based on a query."""
    docs = retriever.invoke(question)
    
    # Combine the results into a single string for the Agent to read
    return "\n\n".join([doc.page_content for doc in docs])


print('✅ Vector database is ready to use.')