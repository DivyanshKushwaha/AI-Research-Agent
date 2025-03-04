# 🚀 AI Agent-Based Deep Research System

This project is a **Deep Research AI Agentic System** that automates online information gathering using **Tavily** and generates structured research summaries using **LangGraph & LangChain**. The system consists of a **FastAPI backend** and a **Streamlit frontend**, providing a seamless and interactive user experience.

The system is built using:

- **LangGraph & LangChain:** for multi-agent workflow
- **Tavily API:** for online data extraction
- **FastAPI** for serving research functionalities
- **Streamlit** as the frontend UI


## ✨ Features
- **Dual-Agent System:** One agent for research and data collection, another for summarization.
- **Tavily Web Search:** Fetches relevant data from the internet.
- **Gemini AI (Google):** Generates well-structured research summaries.
- **FastAPI Backend:** Exposes endpoints for research and summarization.
- **Markdown File Storage:** Saves summaries as `.md` files for easy readability and downloads.

---

## 🛠 Project Structure
```bash
D:/Research-Agent
│   .gitignore
│   README.md
│   requirements.txt│
├───backend
│   │   main.py   # API routes and agent execution 
│   │   models.py  # Helper functions
│   │   research.py   # Tavily-based research agent and LLM-based answer generation 
├───frontend
│   |   app.py  # Frontend Implementation 
└───responses

```

## Implementation

### 1. Dual-Agent System Using LangGraph & LangChain

The system is divided into two AI agents:

**Research Agent (Tavily API Search)**
- Uses TavilySearchResults from LangChain to fetch data from the web.
- Extracts top 5 search results for deeper context.
- Returns raw extracted content to the next agent.


```bash
    from langchain_community.tools.tavily_search import TavilySearchResults

    def search_web(query: str) -> list:
        """Fetches web data using Tavily API."""
        tavily_tool = TavilySearchResults(max_results=5)
        response = tavily_tool.invoke(query)
        return [item["content"] for item in response] if response else ["No relevant information found."]

```


**Answer Agent (LLM-Powered Summarization)**
- Takes extracted research data and formats it into a prompt.
- Uses Gemini AI (via LangChain) to generate structured research summaries.

```bash
    from langchain_google_genai import ChatGoogleGenerativeAI

    # Initialize LLM
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    def generate_answer(research_data: list) -> str:
        """Generates a structured research summary using Gemini AI."""
        formatted_data = "\n\n".join(research_data)
        prompt = f"You are an expert researcher. Based on the following information:\n\n{formatted_data}\n\nGenerate a well-structured summary."

        response = model.invoke(prompt)
        return response.content if response and hasattr(response, "content") else "No response generated."

```

### 2. LangGraph Based Workflow

We use LangGraph to define agent interactions:

- Step 1: The Research Agent fetches data → sends it to the Answer Agent.
- Step 2: The Answer Agent generates a summary → returns the final response.

```bash
    from langgraph.graph import Graph

    graph = Graph()

    graph.add_node("ResearchAgent", search_web)
    graph.add_node("AnswerAgent", generate_answer)

    graph.set_entry_point("ResearchAgent")
    graph.add_edge("ResearchAgent", "AnswerAgent")
    graph.set_finish_point("AnswerAgent")

    exec = graph.compile()


```
### 3. FastAPI for backend

To expose the research functionality, we wrap it inside FastAPI

```bash 
    from fastapi import FastAPI
    from models import QueryRequest, ResearchResponse
    from research import deep_research_system
    import uvicorn
    import os

    app = FastAPI()

    # Ensure response directory exists
    RESPONSES_DIR = "responses"
    os.makedirs(RESPONSES_DIR, exist_ok=True)

    @app.post("/research", response_model=ResearchResponse)
    def research_endpoint(request: QueryRequest):
        """Handles research queries and saves responses."""
        response_text = deep_research_system(request.query)

        # Save response as markdown file
        file_path = os.path.join(RESPONSES_DIR, f"{request.query.replace(' ', '_')}.md")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response_text)

        return {"response": response_text}


    if __name__=="__main__":
        uvicorn.run(app=app)
```

### 4. Streamlit UI for frontend
```bash

    import streamlit as st
    import requests

    st.title("AI Research Assistant")

    query = st.text_input("Enter your research topic:")

    if st.button("Get Research Summary"):
        response = requests.post("http://127.0.0.1:8000/research", json={"query": query})
        
        if response.status_code == 200:
            summary = response.json()["summary"]
            st.markdown(summary)
            
            # Save as markdown
            filename = f"research_outputs/{query.replace(' ', '_')}.md"
            with open(filename, "w") as f:
                f.write(summary)
            st.success(f"Saved summary as {filename}")
        else:
            st.error("Failed to fetch summary. Try again.")


```

## Features & Enhancements
- Automated Research System – No manual web browsing required.
- Structured, AI-Generated Summaries – Well-formatted insights for better understanding.
- FastAPI + Streamlit Integration – Efficient backend & user-friendly frontend.
- Markdown File Storage – Saves summaries for future reference.
- Scalable Design – Easily extendable with more LLMs & features.

## Setup Instructions

### Clone the repository (command in powershell)
```bash
git clone https://github.com/DivyanshKushwaha/AI-Research-Agent.git
```


### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
- Server runs at: `http://127.0.0.1:8000`

### Frontend (Streamlit)
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
- UI available at: `http://localhost:8501`

---

## Environment Variables
Create a `.env` file in the root folder with:
```ini
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## Usage
1. Enter a research query in the Streamlit UI.
2. The backend fetches web data via Tavily and processes it using LangGraph.
3. A structured research summary is generated using Gemini AI.
4. The summary is displayed in the UI and saved as a Markdown file.
5. Users can download the saved `.md` file for reference.

---

## Example Output
```
# Research Summary: AI in Healthcare

## Positive Impacts
- **Improved Access:** AI expands healthcare access in underserved areas.
- **Data-Driven Decisions:** Enhances clinical decisions and personalized medicine.
- **Increased Efficiency:** Automates administrative tasks.

## Challenges & Ethical Concerns
- **Privacy Risks:** Patient data security is critical.
- **Bias in AI Models:** Potential for biased predictions and diagnoses.
.
.
.
.
more

```

---


