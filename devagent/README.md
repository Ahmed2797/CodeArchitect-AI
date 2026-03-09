# CodeArchitect-AI

CodeArchitect AI – Multi-Agent Codebase Intelligence System

## CodeArchitect-AI – Multi-Agent AI Repository Analyzer

**CodeArchitect-AI** is an advanced multi-agent AI system designed to **analyze codebases**, **detect bugs**, **understand system architecture**, and **generate documentation automatically**. It is built using [CrewAI](https://docs.crewai.com), Retrieval-Augmented Generation (RAG), and vector-based code search.

---

## 🛠 Features

- **Code Reader Agent:** Deeply analyzes repository files to map logic, modules, and data flow.
- **Bug Finder Agent:** Detects logic flaws, security vulnerabilities, and PEP8/code style issues.
- **Architect Agent:** Explains system architecture and design patterns.
- **Documentation Agent:** Generates professional README and API documentation automatically.
- **Vector Database Search:** Retrieves relevant code snippets from FAISS or other RAG backends.
- **Multi-Agent Workflow:** Tasks are sequenced with dependencies to produce structured output.

---

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv

---

## ⚡ Installation

# Clone the repository
git clone https://github.com/Ahmed2797/CodeArchitect-AI
cd devagent

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

```bash
from src.devagent.crew import Devagent

# Initialize Crew
devagent = Devagent()

# Create Crew object
crew_system = devagent.crew()  # <- note: call the method to get Crew object

# Run the AI agents on your codebase
result = crew_system.kickoff(
    inputs={"user_question": "Where is the route optimization logic?"}
)

print(result)
```
