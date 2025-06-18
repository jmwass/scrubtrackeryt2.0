import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta

class YouTubeAgent:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def search_youtube(self, query="Scrub Daddy", days_back=7):
        today = datetime.utcnow()
        one_week_ago = today - timedelta(days=days_back)

        published_after = one_week_ago.isoformat("T") + "Z"
        published_before = today.isoformat("T") + "Z"

        search_response = self.youtube.search().list(
            q=query,
            part="snippet",
            maxResults=25,
            type="video",
            order="viewCount",
            publishedAfter=published_after,
            publishedBefore=published_before
        ).execute()

        video_data = []
        exclusion_keywords = ["shark", "shark tank", "sharktank"]

        for item in search_response["items"]:
            title = item["snippet"]["title"].lower()
            description = item["snippet"].get("description", "").lower()

            # Exclude Scrub Daddy's own channel
            if item["snippet"]["channelTitle"].lower() == "scrub daddy":
                continue

            # Exclude based on shark-related keywords
            if any(keyword in title or keyword in description for keyword in exclusion_keywords):
                continue

            video_id = item["id"]["videoId"]
            channel_id = item["snippet"]["channelId"]
            video_data.append({
                "Video ID": video_id,
                "Title": item["snippet"]["title"],
                "Channel ID": channel_id
            })

        return video_data
