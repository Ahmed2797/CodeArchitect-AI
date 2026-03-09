import git
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document 
from langchain_classic.document_loaders import DirectoryLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

def clone_repo(repo_url):
    
    repo_path = "code_analisis_repo"

    if os.path.exists(repo_path):
        return repo_path

    git.Repo.clone_from(repo_url, repo_path)
    return repo_path

# repo = clone_repo("https://github.com/Ahmed2797/Travel-Planner-Agent.git")




def build_vector_db(repo_path):
    print("🔍 Loading code files from the repository...")

    loader = DirectoryLoader(repo_path, glob="**/*.py")
    docs = loader.load()

    print(f"📄 Loaded {len(docs)} code files. Building vector database...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=120,
        chunk_overlap=30
    )

    chunks = splitter.split_documents(docs)

    print(f"📊 Created {len(chunks)} chunks from the code files. Generating embeddings and building FAISS index...")
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small")

    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local("faiss_code_index") 
    print("✅ Vector Index saved to disk.")

    return vector_db



def get_vector_db(index_path="faiss_code_index"):
    if os.path.exists(index_path):
        print("--- Loading existing index from disk ---")
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small")

        return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    else:
        print("--- No index found. Creating new one (this may take time) ---")
        return build_vector_db("code_analisis_repo")

# # Usage in your script:
# vector_db = get_vector_db(chunks, embeddings)
# retriever = vector_db.as_retriever()