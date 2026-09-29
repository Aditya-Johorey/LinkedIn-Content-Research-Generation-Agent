# from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import ollama
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.7
)