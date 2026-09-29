from app.workflows.marketing_workflow import app

response = app.invoke({
    "topic": "AI Agents in Marketing"
})

print(response["content"])