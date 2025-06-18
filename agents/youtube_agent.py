from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

class YouTubeAgent:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def load_video_data(self):
        today = datetime.utcnow()
        one_week_ago = today - timedelta(days=30)

        published_after = one_week_ago.isoformat("T") + "Z"
        published_before = today.isoformat("T") + "Z"

        search_response = self.youtube.search().list(
            q="Scrub Daddy",
            part="snippet",
            maxResults=50,
            type="video",
            order="viewCount",
            publishedAfter=published_after,
            publishedBefore=published_before
        ).execute()

        video_data = []
        for item in search_response["items"]:
            if item["snippet"]["channelTitle"].lower() == "scrub daddy":
                continue  # Exclude official channel

            video_id = item["id"]["videoId"]
            channel_id = item["snippet"]["channelId"]
            video_data.append({
                "video_id": video_id,
                "Title": item["snippet"]["title"],
                "Channel": item["snippet"]["channelTitle"],
                "Channel ID": channel_id,
                "Published": item["snippet"]["publishedAt"],
                "URL": f"https://www.youtube.com/watch?v={video_id}"
            })

        if not video_data:
            return []

        # Add video stats
        video_ids = [v["video_id"] for v in video_data]
        stats_response = self.youtube.videos().list(
            part="statistics",
            id=",".join(video_ids)
        ).execute()

        for i, stats in enumerate(stats_response["items"]):
            video_data[i]["Views"] = int(stats["statistics"].get("viewCount", 0))
            video_data[i]["Likes"] = int(stats["statistics"].get("likeCount", 0))
            video_data[i]["Comments"] = int(stats["statistics"].get("commentCount", 0))

        # Add subscriber count for each channel
        channel_ids = list(set([v["Channel ID"] for v in video_data]))
        channel_stats = self.youtube.channels().list(
            part="statistics",
            id=",".join(channel_ids)
        ).execute()

        subs_dict = {item["id"]: int(item["statistics"].get("subscriberCount", 0)) for item in channel_stats["items"]}
        for v in video_data:
            v["Subscribers"] = subs_dict.get(v["Channel ID"], 0)

        # Filter by creator threshold
        video_data = [v for v in video_data if v["Subscribers"] >= 10000]

        return video_data
