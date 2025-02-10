<a href="https://idx.google.com/import?url=https%3A%2F%2Fgithub.com%2Fapappascs%2Fcrewai-independent-execution">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://cdn.idx.dev/btn/open_dark_32.svg">
    <source
      media="(prefers-color-scheme: light)"
      srcset="https://cdn.idx.dev/btn/open_light_32.svg">
    <img
      height="32"
      alt="Open in IDX"
      src="https://cdn.idx.dev/btn/open_purple_32.svg">
  </picture>
</a>

# IndependentCrew: CrewAI Development Through Isolation

This project is a practical guide to demonstrate the power of **running agents and tasks independently within the CrewAI framework**. While CrewAI excels at orchestrating complex agent collaborations, the ability to isolate and test individual components is invaluable during development. This approach simplifies debugging, accelerates iteration, and promotes a modular design for your AI crews.

## Why Run Agents and Tasks Independently?

**In essence, independent execution is about targeted development and testing.** When building complex CrewAI systems, isolating components provides several practical advantages:

*   **Faster Debugging:** If an agent or task misbehaves, you can test it in isolation without the overhead of the full crew. This simplifies the process of identifying and fixing the root cause.
*   **Reduced Iteration Cycle:** Changes to individual agents or tasks can be validated immediately. You don't need to execute the entire workflow to observe the impact of your modifications.
*   **Improved Code Modularity:** Designing agents and tasks that can function independently encourages a more modular codebase. This makes the system easier to understand, maintain, and extend.
*   **Targeted Performance Analysis:** Profiling and performance optimization can be focused on specific agents or tasks without the noise of the entire crew's execution.

## Getting Started

This project provides a simple yet illustrative example of how to run agents and tasks independently. Here's how to get started:

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

**Install uv:**

```bash
pip install uv
```

**Install CrewAI:**

```bash
pip install crewai crewai-tools
```

**Clone the Repository:**

```bash
git clone https://github.com/apappascs/crewai-independent-execution.git
```

**Install Dependencies:**

```bash
crewai install
```

**Set your API Key:**
Add your `API_KEY` (you can use OpenAI, Gemini or any other supported by CrewAI) into the `.env` file in the root of the project:
```
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

## Project Structure

The project is structured to clearly demonstrate independent execution:

-   `src/independent_crew/config/agents.yaml`: Defines the `researcher` agent.
-   `src/independent_crew/config/tasks.yaml`: Defines the `research_task`.
-   `src/independent_crew/crew.py`: Sets up the `IndependentCrew` class, demonstrating how agents and tasks are typically defined within a crew.
-   `src/independent_crew/tools/custom_tool.py`: Implements a simple `WebSearchTool` for demonstration.
-   `src/independent_crew/main.py`: Contains the code to run the full crew (for comparison).
-   `src/independent_crew/run_agent.py`: **The key script** showing how to run the `researcher` agent independently.
-   `src/independent_crew/run_task.py`: **The key script** showing how to run the `research_task` independently.

## Running the Examples

**1. Running the Full Crew (Optional):**

You can run the full crew (for demonstration purposes) using:

```bash
crewai run
```

This will execute the `research_task` using the `researcher` agent within a crew context.

**2. Running the Agent Independently:**

This is where the magic happens. Run:

```bash
python3 -m src.independent_crew.run_agent
```

The `run_agent.py` script demonstrates two methods:

- **Creating an agent from its configuration** and executing a custom task.
- **Reusing the agent and task definitions** from `crew.py` for a more streamlined approach.

**3. Running the Task Independently:**

Similarly, run:

```bash
python3 -m src.independent_crew.run_task
```

The `run_task.py` script demonstrates:

- Executing a task **synchronously and asynchronously** using a separately created agent.
- **Reusing the task definition** from `crew.py` and providing a custom context.
- Overriding the `agent`, `context`, and `tools` at runtime when using both `execute_sync` and `execute_async`.

## Deep Dive: Independent Agent and Task Execution

Let's explore the core concepts that make independent execution tick:

### Running an Agent Independently

Agents in CrewAI can execute tasks independently without needing to set up a full crew. Here's how you can run an agent independently:

```python
# Create an agent
researcher_agent = Agent(
    role="Research Expert",
    goal="Provide accurate and detailed information on a given topic.",
    backstory="An experienced researcher who has been working for many years.",
    llm="gemini/gemini-1.5-flash",  # Replace with your desired LLM
    verbose=True
)

# Create a task
research_task = Task(
    description="Research the latest trends in AI for autonomous vehicles.",
    expected_output="A detailed report on the topic.",
)

# Execute the task with the agent
output = researcher_agent.execute_task(task=research_task)

print("Task Output:", output)
```

#### Key Parameters for Independent Execution

| Parameter         | Description                                                                                 |
| ------------------| ------------------------------------------------------------------------------------------- |
| `task`            | The task to execute, including its description and expected output.                         |
| `context` _(optional)_ | Additional context or background information that the agent can use during execution.   |
| `tools` _(optional)_   | Tools available to the agent during task execution, which can override the default tools.|

#### Agent Task Execution Implementation

Internally, the `execute_task` method processes the task as follows:

- Combines the task prompt with any additional context or knowledge snippets.
- Uses tools if provided, or defaults to the agent's tools.
- Executes the task using the specified language model.
- Handles retries, memory, and other configurations as specified in the agent attributes.

### Running a Task Independently

To execute a task independently, you need an agent to perform it. CrewAI supports both synchronous and asynchronous execution of tasks.

#### Synchronous Execution

You can execute a task synchronously using the `execute_sync` method. This method ensures the task is completed before moving on to other operations.

```python
# Create a task
research_task = Task(
    description="Research the latest trends in AI for autonomous vehicles.",
    expected_output="A detailed report on the topic.",
    agent=researcher_agent,  # Assign the agent to the task
)
# Execute the task synchronously
output = research_task.execute_sync()
print("Task Output:", output.raw)  # Access the raw output
```

#### Asynchronous Execution

For tasks that are time-consuming or can run in parallel with other operations, you can use the `execute_async` method. This allows you to execute the task asynchronously and retrieve the result later.

```python
from concurrent.futures import Future
# Create a task
research_task = Task(
    description="Research the latest trends in AI for autonomous vehicles.",
    expected_output="A detailed report on the topic.",
    agent=researcher_agent,  # Assign the agent to the task
)
# Execute the task asynchronously
future_output: Future = research_task.execute_async()
# Perform other operations...
# Retrieve the result
output = future_output.result()
print("Task Output:", output.raw)  # Access the raw output
```

#### Key Methods for Execution

The following methods are available for task execution:

| Method              | Description                                                                 |
| --------------------| --------------------------------------------------------------------------- |
| `execute_sync`      | Executes the task synchronously and returns a `TaskOutput` object.          |
| `execute_async`     | Executes the task asynchronously, returning a `Future[TaskOutput]` object. |

#### Example of Context and Tool Overrides

Both `execute_sync` and `execute_async` support overriding the `agent`, `context`, and `tools` at runtime, allowing you to adapt task execution dynamically:

```python
# Execute task with overridden agent, context, and tools
custom_context = "Research related to AI applications in healthcare."
custom_tools = [custom_search_tool] # Assuming you have a custom_search_tool defined
output = research_task.execute_sync(
    agent=custom_agent, # Assuming you have a custom_agent defined
    context=custom_context,
    tools=custom_tools
)
print("Task Output with Custom Context:", output.raw)
```
