import pandas as pd

class AnalyticsAgent:
    def get_engagement(self, video_data):
        try:
            # If input is a list of dicts, convert to DataFrame
            if isinstance(video_data, list):
                df = pd.DataFrame(video_data)
            elif isinstance(video_data, pd.DataFrame):
                df = video_data
            else:
                return "Invalid input: video_data must be a list or DataFrame."

            if df.empty:
                return "No video data available to analyze."

            if "Views" not in df.columns or "Likes" not in df.columns:
                return "Video data missing 'Views' or 'Likes' fields."

            avg_views = df["Views"].mean()
            avg_likes = df["Likes"].mean()
            df["Engagement Rate (%)"] = (df["Likes"] / df["Views"]) * 100

            top_video = df.sort_values(by="Views", ascending=False).iloc[0]
            highest_engagement = df["Engagement Rate (%)"].max()

            summary = (
                f"📊 **YouTube Analytics Summary:**\n\n"
                f"- Total Videos Analyzed: **{len(df)}**\n"
                f"- Average Views: **{avg_views:,.0f}**\n"
                f"- Average Likes: **{avg_likes:,.0f}**\n"
                f"- Top Video: **{top_video['Title']}** with **{top_video['Views']:,}** views\n"
                f"- Highest Engagement Rate: **{highest_engagement:.2f}%**"
            )

            return summary

        except Exception as e:
            return f"Analytics error: {e}"
