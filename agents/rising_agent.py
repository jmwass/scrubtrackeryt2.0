import pandas as pd

class RisingAgent:
    def find_rising_creators(self, video_data):
        try:
            df = pd.DataFrame(video_data)

            if df.empty or "Subscribers" not in df.columns:
                return "No creator data available."

            # Filter criteria
            filtered_df = df[
                (df["Channel"].str.lower() != "scrub daddy") &
                (df["Subscribers"].between(10_000, 50_000)) &
                (df["Views"] > 5000)
            ]

            if filtered_df.empty:
                return "No rising creators found this week."

            grouped = filtered_df.groupby("Channel").agg({
                "Subscribers": "first",
                "Views": "sum",
                "Likes": "sum",
                "URL": "first"
            }).sort_values(by="Views", ascending=False).head(5)

            markdown = "🚀 **Rising Creators to Watch:**\n\n"
            for idx, row in grouped.iterrows():
                markdown += (
                    f"- **{idx}** ({row['Subscribers']:,} subs) — "
                    f"{row['Views']:,} views, {row['Likes']:,} likes  \n"
                    f"🔗 [Recent Video]({row['URL']})\n\n"
                )

            return markdown

        except Exception as e:
            return f"RisingAgent error: {e}"
