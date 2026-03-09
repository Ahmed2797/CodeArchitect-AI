from src.devagent.crew import Devagent
from src.devagent.helper import clone_repo, build_vector_db,get_vector_db




repo = 'https://github.com/Ahmed2797/Travel-Planner-Agent.git'
index = "faiss_code_index"


repo_path = clone_repo(repo)

# vector_db = build_vector_db(repo_path)
vector_db = get_vector_db(index_path=index)  # This will load the existing index if it exists, or create a new one if it doesn't
retriever = vector_db.as_retriever()

# Initialize Crew with YAML configs
crew_system = Devagent()
crew = crew_system.crew()

# Run the crew
result = crew.kickoff(
    inputs={"user_question": "Where is the route optimization logic?"}
)

print(result)