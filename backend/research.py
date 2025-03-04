from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import Graph
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import Tool
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List
import os

# Load API keys from .env
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize LLM
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Web Search Tool
def search_web(query: str) -> list:
    """Fetches web data using Tavily API."""
    tavily_tool = TavilySearchResults(max_results=5)
    response = tavily_tool.invoke(query)
    return [item["content"] for item in response] if response else ["No relevant information found."]

search_tool = Tool(
    name="Web Research Tool",
    func=search_web,
    description="Fetches relevant online information."
)

# Answer Generation
ANSWER_TEMPLATE = """
You are an expert researcher. Based on the following information:

{data}

Generate a well-structured research summary in bullet points with engaging and interactive formatting.
"""

class ResearchDataInput(BaseModel):
    research_data: List[str] = Field(..., description="List of research data.")

def generate_answer(research_data: List[str]) -> str:
    """Generates an interactive research summary."""
    if not research_data:
        return "No relevant data found."

    formatted_data = "\n\n".join(research_data)
    prompt = ANSWER_TEMPLATE.format(data=formatted_data)

    try:
        response = model.invoke(prompt)
        return response.content if response and hasattr(response, "content") else "No response generated."
    except Exception as e:
        return f"Error: {str(e)}"

answer_tool = StructuredTool.from_function(
    func=generate_answer,
    name="generate_answer",
    args_schema=ResearchDataInput,
    description="Generates a well-structured research summary."
)

# Dual-Agent System
def research_agent(inputs):
    """Fetches web research data."""
    query = inputs.get("input", "")
    search_results = search_tool.invoke(query)
    return {"data": search_results}

def answer_agent(inputs):
    """Generates a structured research summary."""
    research_data = inputs.get("data", [])
    response = answer_tool.invoke({"research_data": research_data})
    return {"response": response}

graph = Graph()
graph.add_node("ResearchAgent", research_agent)
graph.add_node("AnswerAgent", answer_agent)
graph.set_entry_point("ResearchAgent")
graph.add_edge("ResearchAgent", "AnswerAgent")
graph.set_finish_point("AnswerAgent")

exec_pipeline = graph.compile()

def deep_research_system(query):
    """Executes the research system and returns response."""
    output = exec_pipeline.invoke({"input": query})
    return output.get("response", "No response generated.")
