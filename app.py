import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
import operator

# 1. Setup Environment
load_dotenv()

# Get Keys
groq_key = os.getenv("GROQ_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

# Safety Check
if not groq_key or not tavily_key:
    st.error("🚨 Configuration Error: API Keys not found!")
    st.write("Make sure your .env file contains: GROQ_API_KEY and TAVILY_API_KEY")
    st.stop()

os.environ["GROQ_API_KEY"] = groq_key
os.environ["TAVILY_API_KEY"] = tavily_key

st.set_page_config(page_title="Deep Research Agent", layout="wide")

st.title("🕵️‍♂️ Autonomous Research Agent")
st.markdown("### Powered by Llama 3.3 (Groq) & LangGraph")

# 2. Define State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# 3. Setup Tools & Model
tool = TavilySearchResults(max_results=2)

# --- CHANGED: Using the NEW Llama 3.3 Model ---
llm = ChatGroq(model="llama-3.3-70b-versatile")

llm_with_tools = llm.bind_tools([tool])

# 4. Define Nodes
def call_model(state: AgentState):
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def call_tool(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    tool_call = last_message.tool_calls[0]
    
    print(f"🔎 Searching for: {tool_call['args']}")
    result = tool.invoke(tool_call['args'])
    
    return {"messages": [AIMessage(content=f"Tool Result: {str(result)}")]}

def should_continue(state: AgentState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 5. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", call_tool)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")
app = workflow.compile()

# 6. UI Logic
user_query = st.text_input("What should I research for you?", placeholder="e.g., Latest breakthroughs in solid state batteries")

if st.button("Start Research"):
    if user_query:
        with st.spinner("Agent is working... (Checking Google, Reading, Summarizing)"):
            initial_state = {
                "messages": [
                    SystemMessage(content="You are a senior researcher. You can use Google Search. Always verify information. When you have the answer, summarize it."),
                    HumanMessage(content=user_query)
                ]
            }
            
            final_state = app.invoke(initial_state)
            
            # Output Cleaning
            last_message = final_state['messages'][-1]
            final_content = last_message.content
            
            st.markdown("### 📝 Research Report")
            st.markdown(final_content)
            
            # Download Button
            st.download_button(
                label="📥 Download Research Report",
                data=str(final_content),
                file_name="research_report.txt",
                mime="text/plain"
            )

            with st.expander("Show Technical Details (Debug Info)"):
                st.write("Raw Output for Developers:")
                st.write(final_state['messages'])