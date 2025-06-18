import streamlit as st
from agents.youtube_agent import YouTubeAgent
from agents.analytics_agent import AnalyticsAgent
from agents.summary_agent import SummaryAgent
import pandas as pd

st.set_page_config(page_title="Scrub Daddy Tracker 2.0", layout="wide")

yt_agent = YouTubeAgent()
analytics_agent = AnalyticsAgent()
summary_agent = SummaryAgent()

st.title("🧽 Scrub Daddy YouTube Tracker 2.0")

# User input prompt
user_input = st.text_input("Ask me something:", placeholder="e.g. Show top videos this week")

# Load video data (mock or real)
videos = yt_agent.load_video_data()

if not isinstance(videos, list) or len(videos) == 0:
    st.warning("No video data found.")
else:
    df = pd.DataFrame(videos)

    lowered = user_input.lower()

    if "top" in lowered or "most viewed" in lowered or "most liked" in lowered:
        def make_clickable(video_id):
            return f"[Watch](https://www.youtube.com/watch?v={video_id})"

        top_views = df.sort_values(by="Views", ascending=False).head(5)
        top_likes = df.sort_values(by="Likes", ascending=False).head(5)

        st.subheader("📈 Top 5 Videos by Views")
        if "video_id" in top_views.columns:
            top_views["Video Link"] = top_views["video_id"].apply(make_clickable)
        st.dataframe(top_views)

        st.subheader("❤️ Top 5 Videos by Likes")
        if "video_id" in top_likes.columns:
            top_likes["Video Link"] = top_likes["video_id"].apply(make_clickable)
        st.dataframe(top_likes)

    elif "summary" in lowered or "recap" in lowered or "week" in lowered:
        summary = summary_agent.summarize(df)
        st.markdown("### 📝 Weekly Summary")
        st.markdown(summary)

    elif "analytics" in lowered or "engagement" in lowered:
        result = analytics_agent.get_engagement(df)
        st.markdown("### 📊 Engagement Stats")
        st.markdown(result)

    elif user_input.strip() != "":
        st.info("Try asking: 'Show top videos', 'Run analytics', or 'Summarize this week'.")
