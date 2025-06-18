import streamlit as st
import pandas as pd
from agents.youtube_agent import YouTubeAgent
from agents.summary_agent import SummaryAgent
from agents.analytics_agent import AnalyticsAgent

# Initialize agents
yt_agent = YouTubeAgent()
summary_agent = SummaryAgent()
analytics_agent = AnalyticsAgent()

st.set_page_config(page_title="Scrub Daddy Agents", page_icon="🧽")
st.title("🧽 Scrub Daddy YouTube Tracker – Agentic Edition")

# Sidebar for view selection
st.sidebar.title("Agent Control Panel")
selected_mode = st.sidebar.radio("Choose a view", ("📊 Dashboard", "🤖 Agent Chat"))

if selected_mode == "📊 Dashboard":
    st.subheader("🔥 Top Videos by Views")
    videos = yt_agent.load_video_data()
    if isinstance(videos, list):
        df = pd.DataFrame(videos)
        top_views = df.sort_values(by="Views", ascending=False).head(10)
        st.dataframe(top_views)

        st.subheader("🔥 Top Videos by Likes")
        top_likes = df.sort_values(by="Likes", ascending=False).head(10)
        st.dataframe(top_likes)
    else:
        st.warning("Could not load video data. Please try again later.")

elif selected_mode == "🤖 Agent Chat":
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
            else:
                st.warning("Could not load video data.")

        elif "summarize" in lowered:
            videos = yt_agent.load_video_data()
            filtered = []
            for video in videos:
                title = video["Title"].lower()
                description = video.get("Description", "").lower()
                if not any(word in title or word in description for word in st.session_state.memory["exclude"]):
                    filtered.append(video)
            if filtered:
                text_to_summarize = "\n".join([f"{v['Title']}: {v.get('Description', '')}" for v in filtered])
                summary = summary_agent.summarize(text_to_summarize)
                st.markdown("**🧼 Summary of top videos this week:**")
                st.markdown(summary)
            else:
                st.warning("No videos available to summarize after filtering.")

        elif "analytics" in lowered or "engagement" in lowered:
            results = analytics_agent.get_engagement(st.session_state.memory["topic"])
            st.markdown(f"**📈 Analytics Results:** {results}")

        elif "exclude shark" in lowered:
            st.session_state.memory["exclude"].append("shark")
            st.session_state.memory["exclude"].append("shark tank")
            st.success("Shark content will now be excluded from summaries.")

        else:
            st.info("Try commands like 'Show me top videos', 'Summarize this week's trends', or 'Filter out Shark Tank'.")
