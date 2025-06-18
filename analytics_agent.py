import random

class AnalyticsAgent:
    def __init__(self):
        pass

    def run(self, prompt):
        # Placeholder logic – this would eventually parse real video stats
        fake_analytics = {
            "avg_views": random.randint(10000, 50000),
            "avg_likes": random.randint(500, 5000),
            "avg_comments": random.randint(20, 300),
            "top_theme": random.choice(["cleansing hacks", "product demos", "reaction collabs"]),
        }

        return (
            f"📊 **Analytics Report**\n"
            f"- Average Views: {fake_analytics['avg_views']}\n"
            f"- Average Likes: {fake_analytics['avg_likes']}\n"
            f"- Average Comments: {fake_analytics['avg_comments']}\n"
            f"- Top Content Theme: *{fake_analytics['top_theme']}*\n"
        )
