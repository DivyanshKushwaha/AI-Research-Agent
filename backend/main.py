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