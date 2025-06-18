from langchain_community.chat_models import ChatGroq
from langchain.schema import HumanMessage
import os

class SummaryAgent:
    def __init__(self):
        self.client = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="mixtral-8x7b-32768"
        )

    def summarize(self, prompt):
        try:
            message = HumanMessage(
                content=f"Please summarize the following YouTube video dataset for the past week:\n\n{prompt}"
            )
            response = self.client([message])
            return response.content
        except Exception as e:
            return f"Summary error: {e}"
