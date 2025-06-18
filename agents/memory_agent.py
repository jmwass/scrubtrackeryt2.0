from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatGroq
from langchain.chains import ConversationChain
import os

class MemoryAgent:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(groq_api_key=self.groq_api_key, model="mixtral-8x7b-32768")

        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=False
        )

    def ask(self, prompt):
        return self.conversation.run(prompt)
