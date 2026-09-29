from tavily import TavilyClient
from dotenv import load_dotenv
import os
load_dotenv()

client = TavilyClient(
    api_key = os.getenv("TAVILY_API_KEY")
)

def search_marketing_trends(query: str):

    print(f"Invoking tavily for searching on the topic: {query}")

    response = client.search(
        query = query,
        search_depth="advanced",
        max_results = 5
    )

    return response["results"]