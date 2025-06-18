import pandas as pd

class AnalyticsAgent:
    def __init__(self):
        pass

    def get_engagement(self, video_data: list[dict]):
        try:
            if not video_data:
                return "No video data available to analyze."

            df = pd.DataFrame(video_data)

            if "Views" not in df.columns or "Likes" not in df.columns:
                return "Video data missing 'Views' or 'Likes' fields."

            avg_views = df["Views"].mean()
            avg_likes = df["Likes"].mean()
            df["Engagement Rate (%)"] = (df["Likes"] / df["Views"]) * 100
            top_video = df.sort_values(by="Views", ascending=False).iloc[0]

            summary = (
                f"📊 **YouTube Analytics Summary:**\n\n"
                f"- Total videos analyzed: {len(df)}\n"
                f"- Average Views: {avg_views:,.0f}\n"
                f"- Average Likes: {avg_likes:,.0f}\n"
                f"- Top Video: \"{top_video['Title']}\" with {top_video['Views']:,.0f} views\n"
                f"- Highest Engagement Rate: {df['Engagement Rate (%)'].max():.2f}%"
            )

            return summary

        except Exception as e:
            return f"Analytics error: {e}"
