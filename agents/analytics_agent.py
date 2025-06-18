import os
import pandas as pd

class AnalyticsAgent:
    def __init__(self):
        pass  # No API keys needed for this one

    def get_engagement(self, video_data_text):
        try:
            # Simulated logic: just count keywords or do basic metrics analysis
            lines = video_data_text.strip().split("\n")
            video_count = len(lines)
            keywords = ["clean", "review", "test", "hack"]
            keyword_hits = {kw: sum(kw in line.lower() for line in lines) for kw in keywords}

            summary = f"Analyzed {video_count} videos. Keyword hits: {keyword_hits}"
            return summary
        except Exception as e:
            return f"Analytics error: {e}"
