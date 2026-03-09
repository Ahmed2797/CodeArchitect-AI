from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file

import yaml
from store import search_codebase

@CrewBase
class Devagent:
    """Devagent crew for repository analysis and documentation generation."""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Load YAML configs
    def __init__(self, agents_yaml="src/devagent/config/agents.yaml", tasks_yaml="src/devagent/config/tasks.yaml"):
        with open(agents_yaml, "r") as f:
            self.agents_config = yaml.safe_load(f)

        with open(tasks_yaml, "r") as f:
            self.tasks_config = yaml.safe_load(f)

        llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
        self.llm = llm

    # ------------------ Agents ------------------ #
    @agent
    def code_reader(self) -> Agent:
        return Agent(
            config=self.agents_config['code_reader'],
            verbose=True,
            llm=self.llm,
            tools=[search_codebase]  # Add the search_codebase tool to the code_reader agent
        )

    @agent
    def bug_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['bug_finder'],
            verbose=True,
            llm=self.llm
        )

    @agent
    def architect(self) -> Agent:
        return Agent(
            config=self.agents_config['architect'],
            verbose=True,
            llm=self.llm
        )

    @agent
    def doc_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['doc_writer'],
            verbose=True,
            llm=self.llm
        )

    # ------------------ Tasks ------------------ #
    @task
    def read_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['read_code_task']
        )

    @task
    def explain_arch_task(self) -> Task:
        return Task(
            config=self.tasks_config['explain_arch_task']
        )

    @task
    def find_bugs_task(self) -> Task:
        return Task(
            config=self.tasks_config['find_bugs_task']
        )

    @task
    def generate_docs_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_docs_task'],
            output_file="readme.md"   
        )

    # ------------------ Crew ------------------ #
    @crew
    def crew(self) -> Crew:
        """Creates the Devagent crew"""
        return Crew(
            agents=self.agents,       # created automatically from @agent
            tasks=self.tasks,         # created automatically from @task
            process=Process.sequential,
            verbose=True,
        )