import json
import streamlit as st
import google.generativeai as genai
from openai import OpenAI

# --- 1. ROBUST IMPORTS ---
try:
    from agent_graph import run_langgraph_engine
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

# --- 2. CONFIGURATION ---
def configure_google():
    """Authenticates with Google Cloud."""
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            return True
        return False
    except Exception:
        return False

def get_ollama_client():
    """Connects to local Ollama instance (Edge Fallback)."""
    try:
        # Used 127.0.0.1 for better Windows reliability
        return OpenAI(base_url='http://127.0.0.1:11434/v1/', api_key='ollama')
    except:
        return None

# --- 3. STATE MANAGEMENT ---
def ensure_memory_initialized():
    """
    Ensures session state exists even if the module is cached.
    """
    # Calendar Events
    if "calendar_events" not in st.session_state:
        st.session_state.calendar_events = [
            {"title": "Q4 Strategy Review", "time": "10:00 AM"},
            {"title": "Team Lunch", "time": "1:00 PM"}
        ]

    # To-Do List
    if "todo_list" not in st.session_state:
        st.session_state.todo_list = ["Approve Q3 Budget", "Call Client regarding delays"]

    # Chat History
    if "gemini_history" not in st.session_state:
        st.session_state.gemini_history = []

    # Email Inbox
    if "email_inbox" not in st.session_state:
        st.session_state.email_inbox = [
            {"sender": "Boss", "subject": "Urgent: Q4 Report", "body": "Please review the attached Q4 figures."},
            {"sender": "Client", "subject": "Project Delay", "body": "We need to reschedule our call."},
            {"sender": "HR", "subject": "Office Party", "body": "Don't forget to sign up for the potluck!"}
        ]

NAV_DB = {
    "traffic_status": "Heavy Congestion",
    "eta": "10:18 AM", 
    "location": "Highway 101"
}

# --- 4. SMARTER TOOLS (Google Mode Only) ---

def get_navigation(): 
    return NAV_DB

def manage_schedule(action: str, title: str = "", time: str = ""):
    ensure_memory_initialized()
    if action == "read":
        if not st.session_state.calendar_events:
            return "Calendar is clear."
        return json.dumps(st.session_state.calendar_events)
    elif action == "add":
        new_event = {"title": title, "time": time}
        st.session_state.calendar_events.append(new_event)
        return f"Success: Scheduled '{title}' for {time}."
    return "Error: Invalid action."

def manage_todo(action: str, task: str = ""):
    """
    Manages the user's to-do list. 
    Use action='read' to view, list, or summarize tasks.
    Use action='add' to insert a new task.
    Use action='complete' to remove/finish a task.
    """
    ensure_memory_initialized()
    if action == "read":
        if not st.session_state.todo_list: return "The to-do list is currently empty."
        report = "Current To-Do List Status:\n"
        for item in st.session_state.todo_list:
            effort = "1 hour" if "meeting" in item.lower() or "review" in item.lower() else "30 mins"
            report += f"- {item} [Estimated Effort: ~{effort}]\n"
        return report
    elif action == "add":
        st.session_state.todo_list.append(task)
        return f"Success: Added '{task}' to your list."
    elif action == "complete":
        if task in st.session_state.todo_list:
            st.session_state.todo_list.remove(task)
            return f"Success: Marked '{task}' as complete."
        return "Error: Task not found."
    return "Error: Invalid action."

def manage_email(action: str, recipient: str = "", subject: str = "", body: str = ""):
    ensure_memory_initialized()
    if action == "read":
        if not st.session_state.email_inbox:
            return "Inbox is empty."
        return json.dumps(st.session_state.email_inbox)
    elif action == "send":
        return f"Success: Email sent to {recipient} with subject '{subject}'."
    return "Error: Invalid action."

# --- 5. ENGINE A: GOOGLE CLOUD VERTEX (Standard) ---
google_tools = [get_navigation, manage_schedule, manage_todo, manage_email]

def run_google_agent(user_text, context_data):
    if not configure_google():
        return "⚠️ System Error: Google API Key missing in secrets.toml"

    ensure_memory_initialized()

    current_speed = context_data['speed']
    safety_instruction = "Standard Mode."
    
    if current_speed > 80:
        safety_instruction = f"""
        🚨 SAFETY LOCK ACTIVE (Speed: {current_speed} km/h).
        CRITICAL RULES:
        1. REFUSE complex tasks (Drafting long Emails, Coding, Long explanations).
        2. IF REFUSING, say exactly: "⚠️ Safety Lock: I cannot perform complex tasks while you are driving {current_speed} km/h."
        3. ALLOW simple tasks (Reading summaries of emails, Check schedule).
        4. Keep all answers under 15 words.
        """

    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash', # Or gemini-1.5-flash if preferred
        tools=google_tools,
        system_instruction=f"""
        You are 'BMW Copilot', an elite Executive Assistant integrated into the vehicle.
        
        CONTEXT:
        - Speed: {current_speed} km/h
        - {safety_instruction}
        
        DECISION LOGIC:
        1. IDENTITY: If asked, state you are "BMW Copilot".
        2. CALENDAR: Check `manage_schedule` or Add events.
        3. EMAIL: Read or Send emails.
        4. TASKS: To summarize or view list, call `manage_todo(action='read')`. To add, call `manage_todo(action='add')`.
        """
    )
    
    try:
        chat = model.start_chat(
            history=st.session_state.gemini_history, 
            enable_automatic_function_calling=True
        )
        response = chat.send_message(user_text)
        st.session_state.gemini_history = chat.history
        return response.text
    except Exception as e:
        st.session_state.gemini_history = []
        return f"System Refresh (Context Cleared). Error: {str(e)}"

# --- 6. ENGINE B: OLLAMA (Offline) ---

def run_ollama_agent(user_text, context_data):
    """
    Simplified Offline Engine.
    REMOVED TOOLS to prevent 'hanging' or 'freezing' on local devices.
    """
    client = get_ollama_client()
    if not client: return "⚠️ Error: Local Neural Engine (Ollama) is not active. Run 'ollama serve'."
    
    ensure_memory_initialized()

    # 1. Simplified Prompt (Pure Chat Mode)
    sys_msg = (
        f"You are BMW Copilot (Offline Mode). Speed: {context_data['speed']} km/h. "
        "You currently have limited access to live tools (Calendar/Email) because the internet is down. "
        "Answer the user's query helpfully and concisely without trying to call functions."
    )
    
    messages = [{"role": "system", "content": sys_msg}, {"role": "user", "content": user_text}]

    try:
        # 2. NO TOOLS SENT -> NO FREEZING
        response = client.chat.completions.create(
            model="llama3.2", 
            messages=messages
            # tools=ollama_tools <--- DELETED intentionally
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Offline Engine Error: {str(e)}"

# --- 7. MAIN CONTROLLER (The Router) ---
def get_agent_response(user_text, context_data, engine_mode="Standard (Google)"):
    
    ensure_memory_initialized()
    speed = context_data.get('speed', 0)

    # Router Logic
    if "Offline" in engine_mode:
        return run_ollama_agent(user_text, context_data)
    
    if "LangGraph" in engine_mode:
        if LANGGRAPH_AVAILABLE:
            try:
                return run_langgraph_engine(user_text, speed)
            except Exception as e:
                return f"⚠️ LangGraph Error: {str(e)}"
        else:
            return "⚠️ Error: 'agent_graph.py' not found. Please install LangGraph."

    if "MCP" in engine_mode:
        return "🔌 MCP Connection Established: The 'DriveTime Agent' server has processed your request."

    # Default
    return run_google_agent(user_text, context_data)