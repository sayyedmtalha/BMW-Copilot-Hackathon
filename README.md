# 🔵 BMW Copilot (DriveSafe OS)

**The Context-Aware Intelligent Assistant for Connected Vehicles.**

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bmw-copilot-hackathon.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![AI Engine](https://img.shields.io/badge/AI-Gemini%20%7C%20Llama-orange)](https://deepmind.google/technologies/gemini/)

## 🚀 Overview

**BMW Copilot** is a hybrid-intelligence agent designed to maximize driver productivity while enforcing strict safety standards. It features a dynamic **Safety Lock** that disables complex cognitive tasks (like drafting emails) when the vehicle speed exceeds 80 km/h, ensuring the driver remains focused on the road.

**🔗 Live Demo:** [Click here to launch the App](https://bmw-copilot-hackathon.streamlit.app/)

The system runs on **DriveSafe OS v2.5**, utilizing a router to switch between cloud-based reasoning (Google Gemini) and offline edge computing (Llama 3.2) based on connectivity and user preference.

---

## ✨ Key Features

### 🛡️ **Adaptive Safety Protocol**
* **Real-time Telemetry:** Monitors vehicle speed via the dashboard slider.
* **Active Safety Lock:** If speed > **80 km/h**, the system enters "Red Alert" mode.
    * *Blocked:* Drafting emails, coding, long explanations.
    * *Allowed:* Checking traffic, reading calendar summaries, simple queries.

### 🧠 **Hybrid AI Architecture**
1.  **Standard Mode (Online):** Powered by **Google Gemini 2.5 Flash**.
    * Full access to live tools: Calendar Management, Email Inbox, and Navigation.
2.  **Offline Mode (Edge):** Powered by **Llama 3.2** (via Ollama).
    * Activates when internet connectivity is lost.
    * **Security Feature:** Tool access is intentionally restricted in this mode to prevent sensitive data (Calendar/Email) from being accessed without a secure cloud handshake.

### 🏗️ **Architectural Prototypes (Roadmap)**
* **LangGraph Reasoning:** A simulation module demonstrating multi-step decision-making workflows (e.g., "Plan a trip based on my meetings").
* **MCP (Model Context Protocol):** A prototype integration showing how future versions will connect to vehicle sensors via standardized protocols.

---

## 📺 Demo Video

[Watch the Demo](https://youtu.be/gYJ1yRGYPkU)

*(Click Watch the demo to watch app demo on YouTube)*

---

## 🛠️ Installation & Setup

Follow these steps to get the application running on your local machine.

### **1. Prerequisites**
* **Python 3.9** or higher.
* **Ollama** installed locally (for Offline Mode support).
    * Download: [ollama.com](https://ollama.com)
* **Google Cloud API Key** (for Standard Mode).

### **2. Clone the Repository**
```bash
git clone [https://github.com/sayyedmtalha/BMW-Copilot-Hackathon.git](https://github.com/sayyedmtalha/BMW-Copilot-Hackathon.git)
cd BMW-Copilot
### **3. Install Python Dependencies**

```bash
pip install -r requirements.txt

```

### **4. Configure Secrets**

Create a file named `.streamlit/secrets.toml` in the root directory and add your Google API key:

```toml
# .streamlit/secrets.toml
GOOGLE_API_KEY = "your_actual_api_key_here"

```

### **5. Prepare the Offline Engine**

Open a terminal and run the following commands to ensure the local model is ready:

```bash
# Pull the Llama 3.2 model
ollama pull llama3.2

# Start the local server
ollama serve

```

*(Keep this terminal window open in the background)*

---

## 🚦 How to Run the App

1. Navigate to the project folder in your terminal.
2. Run the Streamlit application:
```bash
streamlit run app.py

```


3. The app will open in your browser at `http://localhost:8501`.

### **User Guide for Demo**

* **Vehicle Telemetry:** Use the **"Current Speed"** slider in the sidebar.
* Set to **65 km/h** to test normal productivity features (Email/Calendar).
* Set to **120 km/h** to test the **Safety Lock** (try asking "Draft an email").


* **Architecture Selector:**
* Select **Standard (Google)** for the main demo.
* Select **Offline (Ollama)** to test the local fallback.
* Select **LangGraph** or **MCP** to view the architectural prototypes.



---

## 📂 Project Structure

```text
/BMW-Copilot-Hackathon
│
├── app.py                # Main Application UI & Sidebar Logic
├── backend.py            # AI Logic Router (Handles Google, Ollama, & Prototypes)
├── agent_graph.py        # LangGraph Simulation Module (Prototype)
├── requirements.txt      # Project Dependencies
├── logo.png              # Project Branding & Icon
└── README.md             # Documentation

```

---


## ℹ️ Architectural Transparency

To ensure a stable and crash-proof demonstration during the hackathon, this project uses a **Hybrid Implementation strategy**:

1. **Fully Functional:** The **Standard (Google)** and **Offline (Ollama)** modes are fully implemented and functional. The **Safety Logic** is live and reactive.
2. **Simulated Prototypes:** The **LangGraph** and **MCP** modules are implemented as **Architectural Simulations**. They demonstrate the intended latency, data flow, and reasoning steps of our Phase 2 roadmap but do not execute live graph compilations to strictly adhere to dependency constraints during the presentation.

---

**Built for the Amulate Hackathon 2025 by Team AI Mechanics**







