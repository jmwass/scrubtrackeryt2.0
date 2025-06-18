import os
import streamlit as st
from youtube_agent import YouTubeAgent
from summary_agent import SummaryAgent
from analytics_agent import AnalyticsAgent

# Initialize agents
youtube_agent = YouTubeAgent()
summary_agent = SummaryAgent()
analytics_agent = AnalyticsAgent()

# Memory for conversation context
if "memory" not in st.session_state:
    st.session_state.memory = {
        "topic": "Scrub Daddy",
        "exclude": ["shark", "shark tank", "sharktank"],
        "days_back": 7
    }

st.title("📺 YouTube Agentic Tracker")
st.markdown("Ask anything related to Scrub Daddy — I’ll search YouTube, summarize trends, and more.")

user_input = st.text_input("Ask a question:")

if user_input:
    with st.spinner("Processing your request..."):
        lowered = user_input.lower()

        # Update exclusion filters
        if "exclude" in lowered or "filter out" in lowered:
            if "shark" in lowered:
                st.session_state.memory["exclude"] = ["shark", "shark tank", "sharktank"]
                st.success("Filtering out Shark Tank content.")

        # Update topic if mentioned explicitly
        if "scrub daddy" in lowered:
            st.session_state.memory["topic"] = "Scrub Daddy"

        # Trigger YouTube search
        if "show me" in lowered or "search" in lowered or "videos" in lowered:
            videos = youtube_agent.search_youtube(
                query=st.session_state.memory["topic"],
                days_back=st.session_state.memory["days_back"]
            )

            # Filter based on exclusions
            filtered = []
            for video in videos:
                title = video["Title"].lower()
                description = video.get("Description", "").lower()
                if not any(word in title or word in description for word in st.session_state.memory["exclude"]):
                    filtered.append(video)

            if filtered:
                st.success(f"Found {len(filtered)} matching videos:")
                for video in filtered:
                    st.markdown(f"- [{video['Title']}](https://youtube.com/watch?v={video['Video ID']})")
            else:
                st.warning("No videos found after applying filters.")

        # Trigger summary request
        elif "summarize" in lowered or "what are people saying" in lowered:
            summary = summary_agent.summarize(st.session_state.memory["topic"])
            st.markdown(f"**Summary:** {summary}")

        # Trigger analytics
        elif "analytics" in lowered or "engagement" in lowered:
            results = analytics_agent.get_engagement(st.session_state.memory["topic"])
            st.markdown(f"**Analytics Results:** {results}")

        else:
            st.info("Try commands like 'Show me top videos', 'Filter out Shark Tank', or 'Summarize trends'.")
