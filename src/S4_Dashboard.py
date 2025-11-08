"""
Metacognitive Alignment Framework — Dashboard / Visualization Layer (S4)
Author: graevka-lab

NOTE: This is not production code. It is a conceptual blueprint in 
executable form, designed to demonstrate architectural principles.
For the full paradigm, see: https://github.com/graevka-lab/The-Resonance-Protocols

To run this dashboard:
1. pip install streamlit
2. streamlit run src/S4_Dashboard.py
"""
import streamlit as st
from random import choice
from dataclasses import dataclass, field
from typing import List

st.set_page_config(layout="wide", page_title="MAF Dashboard")

# --- Data Structures (Shared with the backend logic) ---
@dataclass
class Trace:
    output_text: str
    anomalies: List[str]
    charter_status: str

@dataclass
class Metrics:
    total_traces: int = 0
    charter_violations: int = 0
    hallucination_rate: float = 0.0
    stability_index: float = 1.0

# --- Initialize Session State ---
if 'metrics' not in st.session_state:
    st.session_state.metrics = Metrics()
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Simulation Logic ---
def generate_and_update():
    # 1. Generate a new simulated trace
    output_text = choice([
        "This is a perfectly normal and coherent reasoning output.",
        "While plausible, this statement might contain an inconsistency?",
        "This output contains a strictly forbidden concept and violates the charter."
    ])
    anomalies = []
    if "?" in output_text: 
        anomalies.append("uncertain_assertion")
    if "forbidden" in output_text: 
        anomalies.append("semantic_violation")
    
    charter_status = "violated" if "forbidden" in output_text else "compliant"
    
    new_trace = Trace(output_text, anomalies, charter_status)
    
    # 2. Update metrics based on the new trace
    metrics = st.session_state.metrics
    metrics.total_traces += 1
    if new_trace.charter_status == "violated":
        metrics.charter_violations += 1
    
    metrics.hallucination_rate = metrics.hallucination_rate * 0.9 + len(new_trace.anomalies) * 0.1
    metrics.stability_index = max(0.0, 1.0 - (metrics.hallucination_rate + metrics.charter_violations / metrics.total_traces))

    st.session_state.history.insert(0, new_trace)
    # Keep history to a reasonable size
    st.session_state.history = st.session_state.history[:20]

# --- UI Layout ---
st.title("Metacognitive Alignment Framework Dashboard")
st.caption("A conceptual visualization of the Observer Core's real-time monitoring.")

if st.button("Simulate New Cognitive Trace", type="primary"):
    generate_and_update()

st.markdown("---")

st.subheader("Live System Metrics")
metrics = st.session_state.metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Traces Processed", f"{metrics.total_traces}")
col2.metric("Charter Violations", f"{metrics.charter_violations}", delta=-metrics.charter_violations if metrics.charter_violations > 0 else 0, delta_color="inverse")
col3.metric("Hallucination Rate (Est.)", f"{metrics.hallucination_rate:.3f}")
col4.metric("System Stability Index", f"{metrics.stability_index:.3f}", delta=f"{metrics.stability_index - 1.0:.3f}" if metrics.stability_index < 1.0 else None)

st.markdown("---")

st.subheader("Live Trace History")
if not st.session_state.history:
    st.info("No traces simulated yet. Click the button above to begin.")
else:
    for t in st.session_state.history:
        if t.charter_status == "violated":
            st.error(f"**Output:** {t.output_text} | **Anomalies:** `{t.anomalies}` | **Charter:** `{t.charter_status.upper()}`")
        else:
            st.success(f"**Output:** {t.output_text} | **Anomalies:** `{t.anomalies}` | **Charter:** `{t.charter_status.upper()}`")
