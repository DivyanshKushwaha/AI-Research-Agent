# 🚀 AI Agent-Based Deep Research System

This project is a **Deep Research AI Agentic System** that automates online information gathering using **Tavily** and generates structured research summaries using **LangGraph & LangChain**. The system consists of a **FastAPI backend** and a **Streamlit frontend**, providing a seamless and interactive user experience.

## ✨ Features
- **Dual-Agent System:** One agent for research and data collection, another for summarization.
- **Tavily Web Search:** Fetches relevant data from the internet.
- **Gemini AI (Google):** Generates well-structured research summaries.
- **FastAPI Backend:** Exposes endpoints for research and summarization.
- **Streamlit Frontend:** User-friendly interface for query input and displaying results.
- **Markdown File Storage:** Saves summaries as `.md` files for easy readability and downloads.

---

## 🛠 Project Structure
```bash
D:/Research-Agent
│   .gitignore
│   README.md
│   requirements.txt│
├───backend
│   │   main.py
│   │   models.py
│   │   research.py
├───frontend
│   |   app.py
└───responses

```

---

## 🚀 Setup Instructions

### Clone the repository (command in powershell)
```bash
git clone https://github.com/DivyanshKushwaha/AI-Research-Agent.git
```


### 1️⃣ Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
- Server runs at: `http://127.0.0.1:8000`

### 2️⃣ Frontend (Streamlit)
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
- UI available at: `http://localhost:8501`

---

## 🔑 Environment Variables
Create a `.env` file in the root folder with:
```ini
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## 📌 Usage
1. Enter a research query in the Streamlit UI.
2. The backend fetches web data via Tavily and processes it using LangGraph.
3. A structured research summary is generated using Gemini AI.
4. The summary is displayed in the UI and saved as a Markdown file.
5. Users can download the saved `.md` file for reference.

---

## 📄 Example Output
```
# Research Summary: AI in Healthcare

## Positive Impacts
- **Improved Access:** AI expands healthcare access in underserved areas.
- **Data-Driven Decisions:** Enhances clinical decisions and personalized medicine.
- **Increased Efficiency:** Automates administrative tasks.

## Challenges & Ethical Concerns
- **Privacy Risks:** Patient data security is critical.
- **Bias in AI Models:** Potential for biased predictions and diagnoses.
```

---

## 🎯 Future Enhancements
- ✅ Improve LLM responses with more contextual insights.
- ✅ Add multi-agent collaboration for deeper research.
- ✅ Implement user authentication for saved research access.

🔗 **Developed using LangGraph, LangChain, FastAPI, Streamlit, Tavily, and Gemini AI.** 🚀
