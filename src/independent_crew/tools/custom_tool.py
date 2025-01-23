from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class WebSearchToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    query: str = Field(..., description="The search query")


class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "A tool that can be used to search the web."
    args_schema: Type[BaseModel] = WebSearchToolInput

    def _run(self, query: str) -> str:
        """Search the web for information."""
        print(f"Simulating web search for: {query}")
        return f"Search results for: {query} - This is a simulated result."
