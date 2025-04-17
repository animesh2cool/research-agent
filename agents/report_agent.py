from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

class ReportAgent:
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2")

    def generate_report(self, analysis, query):
        prompt = PromptTemplate(
            input_variables=["analysis", "query"],
            template="""
Create a final user-friendly research report based on the following analysis for the query: "{query}".

Analysis:
----------
{analysis}

Now write the final report in markdown format with a title, summary, and conclusion.
"""
        )

        chain = prompt | self.llm
        return chain.invoke({"analysis": analysis, "query": query})
