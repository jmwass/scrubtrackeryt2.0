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

user_input = st.text_input("Ask me something:", placeholder="e.g. Show top videos this week")

# Load YouTube data
videos = yt_agent.load_video_data()

if not isinstance(videos, list) or len(videos) == 0:
    st.warning("No video data found.")
else:
    df = pd.DataFrame(videos)

    def make_video_link(video_id, title):
        return f"[{title}](https://www.youtube.com/watch?v={video_id})"

    def format_creator(name, subs):
        return f"{name} ({subs} subscribers)" if subs else name

    if "video_id" in df.columns and "Title" in df.columns:
        df["Video"] = df.apply(lambda row: make_video_link(row["video_id"], row["Title"]), axis=1)

    if "Channel" in df.columns and "Subscribers" in df.columns:
        df["Creator"] = df.apply(lambda row: format_creator(row["Channel"], row["Subscribers"]), axis=1)
    elif "Channel" in df.columns:
        df["Creator"] = df["Channel"]

    # Process query
    lowered = user_input.lower()

    if "top" in lowered or "most viewed" in lowered or "most liked" in lowered:
        st.subheader("📈 Top 5 Videos by Views")
        top_views = df.sort_values(by="Views", ascending=False).head(5)
        st.dataframe(top_views[["Video", "Creator", "Views", "Likes"]])

        st.subheader("❤️ Top 5 Videos by Likes")
        top_likes = df.sort_values(by="Likes", ascending=False).head(5)
        st.dataframe(top_likes[["Video", "Creator", "Views", "Likes"]])

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
