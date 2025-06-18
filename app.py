import streamlit as st
from agents.youtube_agent import YouTubeAgent
from agents.summary_agent import SummaryAgent
from agents.analytics_agent import AnalyticsAgent

st.set_page_config(page_title="Scrub Daddy Agents", page_icon="🧽")
st.title("🧽 Scrub Daddy YouTube Tracker – Agentic Edition")

# Initialize agents
yt_agent = YouTubeAgent()
summary_agent = SummaryAgent()
analytics_agent = AnalyticsAgent()

# Sidebar for interaction
st.sidebar.title("Agent Control Panel")
selected_agent = st.sidebar.radio("Choose an agent", ("YouTubeAgent", "SummaryAgent", "AnalyticsAgent"))

# Chat interface
st.subheader("🤖 Ask a Question")
user_input = st.text_input("Type your prompt here...")

if user_input:
    if selected_agent == "YouTubeAgent":
        response = yt_agent.run(user_input)
    elif selected_agent == "SummaryAgent":
        response = summary_agent.run(user_input)
    elif selected_agent == "AnalyticsAgent":
        response = analytics_agent.run(user_input)
    else:
        response = "Unknown agent."

    st.markdown("### 💬 Agent Response")
    st.write(response)
