from app.core.llm import llm
from app.models.content_models import LinkedInPost

structured_llm = llm.with_structured_output(
    LinkedInPost
)

def content_node(state):

    topic = state["topic"]
    research = state["research"]

    print(f"Starting the content creation on the topic {topic}")

    prompt = f"""
    Create a high-quality LinkedIn post.

    Topic:
    {topic}

    Research:
    {research}
    """

    result = structured_llm.invoke(prompt)

    state["content"] = result

    return state