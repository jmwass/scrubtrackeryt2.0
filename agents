import os
import requests
from datetime import datetime, timedelta

class YouTubeAgent:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.base_url = "https://www.googleapis.com/youtube/v3/search"

    def run(self, prompt):
        if "scrub daddy" not in prompt.lower():
            return "Please include 'Scrub Daddy' in your search query."

        # Set time window: last 7 days
        published_after = (datetime.utcnow() - timedelta(days=7)).isoformat("T") + "Z"

        params = {
            "part": "snippet",
            "q": "Scrub Daddy",
            "type": "video",
            "order": "viewCount",
            "publishedAfter": published_after,
            "maxResults": 10,
            "key": self.api_key
        }

        response = requests.get(self.base_url, params=params)
        if response.status_code != 200:
            return f"Failed to fetch from YouTube API: {response.status_code}"

        items = response.json().get("items", [])
        results = []

        for item in items:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Filter out Scrub Daddy's official channel
            if "Scrub Daddy" not in channel:
                results.append(f"- [{title}]({video_url}) by **{channel}**")

        if not results:
            return "No trending Scrub Daddy videos found (outside the brand channel)."

        return "\n".join(results)
