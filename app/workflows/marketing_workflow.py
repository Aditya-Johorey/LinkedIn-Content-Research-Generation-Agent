from langgraph.graph import StateGraph
from app.workflows.state import MarketingState

from app.agents.research_agent import research_node
from app.agents.content_agent import content_node

workflow = StateGraph(MarketingState)

workflow.add_node(
    "research",
    research_node
)

workflow.add_node(
    "content",
    content_node
)

workflow.set_entry_point("research")

workflow.add_edge(
    "research",
    "content"
)

workflow.set_finish_point("content")

app = workflow.compile()