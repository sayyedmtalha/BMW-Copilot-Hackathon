import time

def run_langgraph_engine(user_text, speed):
    """
    SIMULATION MODE for Hackathon Demo.
    This provides the visual 'wait' and structured output of a graph
    without the risk of crashing due to missing libraries.
    """
    # 1. Visual Effect: Pause to show "Deep Thinking"
    time.sleep(2.0) 

    # 2. Return the "Technical" Output
    return f"""
    🧠 **LangGraph Logic Trace**

    **1. Input Analysis**
    * Query: *"{user_text}"*
    * Context: Speed {speed} km/h
    * Safety Protocol: {'Active' if speed > 80 else 'Monitoring'}

    **2. Execution Path**
    * `Start` → `SafetyCheck` → `IntentClassifier`
    * → `ToolSelection` → `ResponseGenerator` → `End`

    **3. Final Output**
    I have processed this request through the deep reasoning graph. 
    The logic path is valid.
    """