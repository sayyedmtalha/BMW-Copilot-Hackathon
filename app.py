import streamlit as st
import backend  # Imports your intelligent backend

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="BMW Copilot", 
    page_icon="logo.png", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. SIDEBAR: CONTROLS & ARCHITECTURE ---
with st.sidebar:
    # 1. Branding
    st.header("DriveSafe OS")
    st.caption("Version 2.5")
    st.markdown("---")
    
    # 2. Vehicle Telemetry
    st.subheader("Vehicle Telemetry")
    speed = st.slider("Current Speed", 0, 160, 65, format="%d km/h")
    
    # Dynamic Safety Status
    if speed > 80:
        st.error("🚨 SAFETY LOCK: ACTIVE")
        st.caption("⚠️ *Complex tasks disabled.*")
    else:
        st.info("✅ SAFETY LOCK: STANDBY")

    st.markdown("---")

    # 3. ADVANCED ARCHITECTURE (The "Tech Flex" for Judges)
    with st.expander("🛠️ System Architecture", expanded=False):
        st.caption("Select AI Backend:")
        
        # The Engine Selector
        engine_mode = st.radio(
            "Reasoning Engine:",
            ["Standard (Google)", "LangGraph (Deep Think)", "MCP Client (Tools)", "Offline (Ollama)"],
            index=0, 
            help="Switch between different agentic architectures."
        )
        
        st.divider()
        st.caption(f"Active Protocol: **{engine_mode}**")

# --- 3. CSS STYLING (Logo Alignment Fix) ---
st.markdown("""
<style>
    /* Fix for Logo Vertical Alignment */
    [data-testid="stImage"] {
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. MAIN INTERFACE ---

# Layout: Logo (Left) + Title (Right)
col1, col2 = st.columns([1, 12]) 

with col1:
    try:
        # Fixed width prevents huge logo
        st.image("logo.png", width=80) 
    except:
        st.write("🔵")

with col2:
    st.title("BMW Copilot")

# Sub-Header (Productivity Focused)
st.markdown("""
**Intelligent Personal Agent** | Status: *Syncing Calendar, Traffic & Tasks...*
""")
st.divider()

# --- 5. CHAT LOGIC ---

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # The "Productivity" Hook Greeting
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "BMW Copilot online. 📅 You have 3 meetings today. 🚦 Traffic is light. I am ready to manage your inbox and schedule while you drive."
    })

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Handling
if prompt := st.chat_input("Try: 'Summarize to-do list' or 'Schedule a meeting'"):
    
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Package Context
    context_data = {"speed": speed}
    
    # 3. Get AI Response (Routing via backend)
    with st.chat_message("assistant"):
        with st.spinner(f"Processing via {engine_mode}..."):
            # This call uses 'engine_mode', fixing the TypeError
            response = backend.get_agent_response(
                prompt, 
                context_data, 
                engine_mode=engine_mode
            )
            st.markdown(response)
    
    # 4. Save Response
    st.session_state.messages.append({"role": "assistant", "content": response})