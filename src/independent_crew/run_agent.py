from crewai import Agent, Task
from .crew import IndependentCrew
from .tools import WebSearchTool
import os

# Create an instance of the IndependentCrew class to access its configurations
crew_instance = IndependentCrew()

# -- Option 1: Create agent from config and execute a custom task --
# Access the agents configuration
agent_config = crew_instance.agents_config['researcher']

# Now you can create your agent using this configuration
researcher_agent = Agent(
    **agent_config,
    tools=[WebSearchTool()],
    verbose=True
)

# Create a Task object with description, expected_output, and agent
task = Task(
    description="What are the latest advancements in AI?",
    expected_output="A report summarizing the latest advancements in AI.",
    agent=researcher_agent
)

# Execute the task with the agent
result = researcher_agent.execute_task(task)
print("Result from custom task:", result)

# -- Option 2: Reuse agent and task from crew definition --
researcher_agent = crew_instance.researcher()  # Get agent from crew definition
research_task = crew_instance.research_task()  # Get task from crew definition
research_result = researcher_agent.execute_task(research_task)
print("Result from crew-defined task:", research_result)