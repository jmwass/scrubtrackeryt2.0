import os
from langchain_community.chat_models import ChatGroq
from langchain.schema import HumanMessage

class SummaryAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing in environment variables.")
        self.client = ChatGroq(
            groq_api_key=self.api_key,
            model="mixtral-8x7b-32768"
        )

    def summarize(self, prompt):
        try:
            messages = [
                HumanMessage(content=f"Please summarize the following:\n\n{prompt}")
            ]
            response = self.client(messages)
            return response.content
        except Exception as e:
            return f"SummaryAgent error: {e}"
