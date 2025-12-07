# 🕵️‍♂️ Autonomous Deep Research Agent

> **A cyclic AI agent that performs autonomous deep web research, verifies facts, and compiles professional reports using Llama 3.3 & LangGraph.**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)
![Groq](https://img.shields.io/badge/Model-Llama3.3-purple.svg)

---

## 📖 Overview

Standard chatbots (like ChatGPT or Gemini) are "one-shot" systems—they guess the answer immediately based on training data. This often leads to hallucinations or outdated information.

The **Deep Research Agent** is different. It is an **Agentic System** that "thinks" in a loop:
1.  It **Plans** a search strategy.
2.  It **Browses** the live internet (using Tavily API).
3.  It **Reads & Analyzes** the results.
4.  It **Decides** if the information is sufficient. If not, it **Loops back** to search again.
5.  It **Compiles** a final, cited report.

## ✨ Key Features

* **⚡ Powered by Groq (LPU):** Utilizes the **Llama-3.3-70b-versatile** model running on Groq's Language Processing Units (LPUs) for near-instant inference speed.
* **🔄 Cyclic Reasoning (LangGraph):** Implements a state-graph architecture allowing the AI to self-correct and perform multi-step research.
* **🌐 Real-Time Web Access:** Connects to the **Tavily Search API** to fetch the latest news, stock prices, and technical documentation.
* **📝 Automated Reporting:** Generates a structured research report that users can **download as a text file**.
* **🔍 Transparent Logic:** Includes a "Debug Mode" (Expandable Sidebar) to view the agent's internal thought process and raw API outputs.
* **🎨 Custom UI:** Features a modern, split-theme Streamlit interface with high-contrast typography and custom CSS styling.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend:** Streamlit
* **Orchestration:** LangGraph (StateGraph)
* **LLM (Brain):** Llama 3.3 (via Groq Cloud)
* **Tools:** Tavily Search API
* **Environment Management:** Python-Dotenv

---

## 🚀 Installation & Setup

Follow these steps to run the agent locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/Antheron23/Autonomous-Deep-Research-Agent.git](https://github.com/Antheron23/Autonomous-Deep-Research-Agent.git)
cd Autonomous-Deep-Research-Agent

2. Install Dependencies
Bash

pip install -r requirements.txt
3. Configure API Keys
This project requires API keys for the LLM and the Search Tool.

Create a file named .env in the root folder.

Add your keys (Get them for free at console.groq.com and tavily.com):

Code snippet

GROQ_API_KEY=gsk_your_groq_key_here
TAVILY_API_KEY=tvly-your_tavily_key_here
4. Run the Application
Bash

streamlit run app.py
🧠 Architecture Flow
Code snippet

graph TD
    A[Start] --> B(Agent Node / Llama 3)
    B --> C{Decide: Tool or Answer?}
    C -- Needs Info --> D[Tool Node / Tavily Search]
    D --> B
    C -- Has Answer --> E[Final Response]
