from datetime import datetime, timedelta
import pandas as pd

class RisingAgent:
    def find_rising_creators(self, video_data):
        try:
            # Convert to DataFrame
            df = pd.DataFrame(video_data)

            if df.empty or "Subscribers" not in df.columns:
                return "No creator data available."

            # Filter creators: not Scrub Daddy, 10k–50k subs, recent videos
            df = df[
                (df["Channel"].str.lower() != "scrub daddy") &
                (df["Subscribers"].between(10_000, 50_000)) &
                (df["Views"] > 5000)
            ]

            if df.empty:
                return "No rising creators found this week."

            # Group by channel, aggregate views/likes
            grouped = df.groupby("Channel").agg({
                "Subscribers": "first",
                "Views": "sum",
                "Likes": "sum",
                "URL": "first"
            }).sort_values(by="Views", ascending=False).head(5)

            markdown = "🚀 **Rising Creators to Watch:**\n\n"
            for idx, row in grouped.iterrows():
                markdown += (
                    f"- **{idx}** ({row['Subscribers']:,} subs) — "
                    f"**{row['Views']:,} views**, {row['Likes']:,} likes  
                    🔗 [Recent Video]({row['URL']})\n"
                )

            return markdown

        except Exception as e:
            return f"Rising Agent Error: {e}"
