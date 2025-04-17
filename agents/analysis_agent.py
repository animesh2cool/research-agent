from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap, RunnableLambda

class AnalysisAgent:
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2", base_url = "http://localhost:11434")

    def analyze(self, text, query):
        prompt = PromptTemplate(
            input_variables=["query", "text"],
            template="""
You are an AI analyst. Based on the user's query: "{query}", summarize and analyze the following content:
------------------
{text}
------------------
Give a concise summary and highlight any relevant insights.
"""
        )

        chain = prompt | self.llm
        return chain.invoke({"query": query, "text": text})
