import os
from openai import OpenAI

class SummaryAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        self.client = OpenAI(api_key=self.api_key)

    def summarize(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful YouTube analytics assistant that summarizes content."},
                    {"role": "user", "content": f"Please summarize the following YouTube content:\n\n{prompt}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"SummaryAgent error: {e}"
