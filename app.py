import streamlit as st
from agents.youtube_agent import YouTubeAgent
from agents.analytics_agent import AnalyticsAgent
from agents.summary_agent import SummaryAgent
import pandas as pd
from agents.rising_agent import RisingAgent

# Page setup
st.set_page_config(page_title="Scrub Daddy Tracker 2.0", layout="wide")
st.title("🧽 Scrub Daddy YouTube Tracker 2.0")

# Load agents
yt_agent = YouTubeAgent()
analytics_agent = AnalyticsAgent()
rising_agent = RisingAgent()
summary_agent = SummaryAgent()

# Load data
videos = yt_agent.load_video_data()

if not videos:
    st.warning("No video data found.")
else:
    df = pd.DataFrame(videos)

    user_input = st.text_input("💬 Ask a question (e.g. 'top videos', 'summary', 'analytics'):")

    if user_input:
        lowered = user_input.lower()

        # === Top Videos by Views ===
        if "top" in lowered or "views" in lowered or "most viewed" in lowered:
            st.subheader("📈 Top 5 Videos by Views")
            top_views = df.sort_values(by="Views", ascending=False).head(5)

            for _, row in top_views.iterrows():
                st.markdown(
                    f"""
                    **{row['Title']}**  
                    👤 Channel: {row['Channel']} ({row.get('Subscribers', 'N/A')} subscribers)  
                    👀 Views: {row['Views']:,} 👍 Likes: {row['Likes']:,}  
                    🔗 [▶️ Watch on YouTube]({row['URL']})
                    ---
                    """,
                    unsafe_allow_html=True
                )

        # === Top Videos by Likes ===
        elif "likes" in lowered or "liked" in lowered:
            st.subheader("❤️ Top 5 Videos by Likes")
            top_likes = df.sort_values(by="Likes", ascending=False).head(5)

            for _, row in top_likes.iterrows():
                st.markdown(
                    f"""
                    **{row['Title']}**  
                    👤 Channel: {row['Channel']} ({row.get('Subscribers', 'N/A')} subscribers)  
                    👀 Views: {row['Views']:,} 👍 Likes: {row['Likes']:,}  
                    🔗 [▶️ Watch on YouTube]({row['URL']})
                    ---
                    """,
                    unsafe_allow_html=True
                )

    elif "summary" in lowered or "summarize" in lowered:
        st.subheader("📝 Weekly Summary")
        text_to_summarize = "\n".join([f"{v['Title']}: {v.get('Description', '')}" for v in videos])
        result = summary_agent.summarize(text_to_summarize)
        st.markdown(result)

    elif "analytics" in lowered or "engagement" in lowered:
        st.subheader("📊 Engagement Analytics")
        results = analytics_agent.get_engagement(videos)
        st.markdown(results)

    elif "rising" in lowered or "reach out" in lowered or "up and coming" in lowered:
        st.subheader("🌱 Rising Creators to Watch")
        result = rising_agent.find_rising_creators(videos)
        st.markdown(result, unsafe_allow_html=True)

    else:
        st.info("Try asking things like: 'top videos', 'most liked', 'summary', 'analytics', or 'rising creators'.")
