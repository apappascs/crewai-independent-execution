from crewai import Agent, Task
from .crew import IndependentCrew
from .tools import WebSearchTool
from concurrent.futures import Future
import os

# Create an instance of the IndependentCrew class to access its configurations
crew_instance = IndependentCrew()

# -- Option 1: Create task from config and execute with a created agent --

# Access the agents configuration
agent_config = crew_instance.agents_config['researcher']

# Now you can create your agent using this configuration
researcher_agent = Agent(
    **agent_config,
    tools=[WebSearchTool()],
    verbose=True
)

# Access the tasks configuration
research_task_config = crew_instance.tasks_config['research_task']

# Create the task using its configuration
research_task = Task(
    **research_task_config,
    verbose=True
)

# Execute the task synchronously
output = research_task.execute_sync(agent=researcher_agent)
print("Synchronous Task Output:", output.raw)

# Execute the task asynchronously
future_output: Future = research_task.execute_async(agent=researcher_agent)
# Perform other operations...

# Retrieve the result
output = future_output.result()
print("Asynchronous Task Output:", output.raw)

custom_context = "Focus on AI in healthcare for the year 2023."
custom_tools = []  # You can add or remove tools here

output = research_task.execute_sync(
    agent=researcher_agent,
    context=custom_context,
    tools=custom_tools
)
print("Task Output with Custom Context:", output.raw)

# -- Option 2: Reuse task from crew definition and provide custom context --
research_task = crew_instance.research_task()
result = research_task.execute_sync(context="What are the ethical implications of AI?", agent=researcher_agent)
print("Task result with custom context:", result)