from app.tools.search_tool import search_marketing_trends

def research_node(state):


    topic  = state['topic']

    print(f"Starting research on topic: {topic}")
    
    result = search_marketing_trends(
        f"Latest trends in {topic}"
    )

    state["research"] = result

    return state