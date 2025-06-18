import os
import streamlit as st
import pandas as pd
from agents.youtube_agent import YouTubeAgent
from agents.summary_agent import SummaryAgent
from agents.analytics_agent import AnalyticsAgent

# App title and layout
st.set_page_config(page_title="Scrub Daddy Tracker 2.0", layout="wide")
st.title("🧽 Scrub Daddy YouTube Tracker – Agentic Edition")

# Initialize agents
yt_agent = YouTubeAgent()
summary_agent = SummaryAgent()
analytics_agent = AnalyticsAgent()

# Sidebar navigation
selected_mode = st.sidebar.selectbox("Choose a mode", ["📊 Weekly Overview", "💬 Agent Chat"])

# Weekly Overview Mode
if selected_mode == "📊 Weekly Overview":
    st.subheader("🔥 Top Videos by Views")
    videos = yt_agent.load_video_data()

    if isinstance(videos, list):
        df = pd.DataFrame(videos)
        top_views = df.sort_values(by="Views", ascending=False).head(10)

        # Create clickable video links
        def make_clickable(video_id):
            return f"[Link](https://www.youtube.com/watch?v={video_id})"

        top_views["Video Link"] = top_views["video_id"].apply(make_clickable)
        st.dataframe(top_views[["Title", "Views", "Likes", "Video Link"]], use_container_width=True)

        st.subheader("🔥 Top Videos by Likes")
        top_likes = df.sort_values(by="Likes", ascending=False).head(10)
        top_likes["Video Link"] = top_likes["video_id"].apply(make_clickable)
        st.dataframe(top_likes[["Title", "Views", "Likes", "Video Link"]], use_container_width=True)
    else:
        st.warning("Could not load video data. Please try again later.")

# Agent Chat Mode
elif selected_mode == "💬 Agent Chat":
    st.subheader("💬 Ask a Question")
    user_input = st.text_input("Type your prompt here...")

    if "memory" not in st.session_state:
        st.session_state.memory = {"topic": "Scrub Daddy", "exclude": ["shark", "shark tank"]}

    if user_input:
        lowered = user_input.lower()

        if "top videos" in lowered:
            videos = yt_agent.load_video_data()
            if isinstance(videos, list):
                df = pd.DataFrame(videos)
                top_views = df.sort_values(by="Views", ascending=False).head(10)
                st.session_state.memory["topic"] = "\n".join([f"{v['Title']}: {v['Description']}" for v in videos])
                st.markdown("**Top 10 Videos by Views:**")
                st.dataframe(top_views)
        elif "summarize" in lowered or "what are people saying" in lowered:
            summary = summary_agent.summarize(st.session_state.memory["topic"])
            st.markdown(f"**Summary:** {summary}")
        elif "analytics" in lowered or "engagement" in lowered:
            results = analytics_agent.get_engagement(st.session_state.memory["topic"])
            st.markdown(f"**Analytics Results:** {results}")
        else:
            st.info("Try commands like 'Show me top videos', 'Summarize this week's trends', or 'Filter out Shark Tank.'")
