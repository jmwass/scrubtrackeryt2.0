import os
from openai import OpenAI

class SummaryAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def summarize(self, prompt):  # ✅ renamed from 'run' to 'summarize'
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a YouTube analytics summarizer."},
                    {"role": "user", "content": f"Please summarize the following:\n\n{prompt}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Summary error: {e}"
