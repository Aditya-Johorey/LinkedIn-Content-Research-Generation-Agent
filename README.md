# LinkedIn Content Research & Generation Agent

An AI-powered content generation pipeline that researches current marketing trends for a given topic and uses the research to generate a structured LinkedIn post.

The project is built around **LangGraph**, with separate research and content-generation nodes, **Tavily** for web research, and a locally hosted **Llama 3.1 8B model through Ollama** for content generation.

---

## Overview

Creating a high-quality LinkedIn post often requires two separate tasks:

1. Researching the latest information and trends around a topic.
2. Turning that research into engaging LinkedIn content.

This project separates these responsibilities into two nodes in a LangGraph workflow:

```text
                Topic
                  │
                  ▼
        ┌──────────────────┐
        │  Research Agent   │
        │                  │
        │ Tavily Web Search│
        └────────┬─────────┘
                 │
                 │ Research Results
                 ▼
        ┌──────────────────┐
        │  Content Agent    │
        │                  │
        │ Llama 3.1 8B     │
        │     + Ollama     │
        └────────┬─────────┘
                 │
                 ▼
          Structured Output
          ┌────────────────┐
          │ Title          │
          │ Hook           │
          │ Body           │
          │ Hashtags       │
          └────────────────┘
```

---

## Key Features

* **Agentic workflow orchestration** using LangGraph
* **Real-time web research** using Tavily
* **Local LLM inference** using Ollama and Llama 3.1 8B
* **Structured LLM output** using Pydantic models
* Modular agent architecture
* Typed workflow state using `TypedDict`
* ChromaDB-based persistent vector-store infrastructure
* Ollama-based text embeddings using `nomic-embed-text`

---

## Tech Stack

| Component              | Technology                |
| ---------------------- | ------------------------- |
| Programming Language   | Python                    |
| Agent Orchestration    | LangGraph                 |
| LLM Framework          | LangChain                 |
| LLM                    | Llama 3.1 8B              |
| Local LLM Runtime      | Ollama                    |
| Web Research           | Tavily                    |
| Structured Output      | Pydantic                  |
| Vector Store           | ChromaDB                  |
| Embeddings             | Ollama `nomic-embed-text` |
| Environment Management | python-dotenv             |

---

## Architecture

The application is divided into several components.

```text
app/
├── agents/
│   ├── research_agent.py
│   └── content_agent.py
│
├── core/
│   └── llm.py
│
├── memory/
│   ├── embeddings.py
│   └── vector_store.py
│
├── models/
│   └── content_models.py
│
├── tools/
│   └── search_tool.py
│
└── workflows/
    ├── marketing_workflow.py
    └── state.py

main.py
requirements.txt
```

### `agents/`

Contains the individual workflow nodes.

#### Research Agent

`research_agent.py` receives the requested topic and sends a query to Tavily:

```text
Latest trends in <topic>
```

The search returns up to five results using Tavily's advanced search depth.

The results are then stored in the workflow state under:

```python
state["research"]
```

#### Content Agent

`content_agent.py` receives both:

* the original topic
* the research results

It passes these to the local Llama 3.1 8B model and requests a structured LinkedIn post.

---

### `core/`

Contains the LLM configuration.

The current implementation uses:

```text
Llama 3.1 8B
      ↓
   Ollama
      ↓
 LangChain ChatOllama
```

This allows the application to perform inference locally rather than requiring a cloud LLM API.

---

### `memory/`

Contains the vector-store infrastructure.

The project initializes a persistent ChromaDB collection:

```text
./chroma_db
```

with the collection:

```text
marketing_memory
```

The project also defines an Ollama embedding model using:

```text
nomic-embed-text
```

This provides the foundation for persistent semantic memory/retrieval.

---

### `models/`

Defines the structured output schema for generated LinkedIn posts.

```python
class LinkedInPost(BaseModel):
    title: str
    hook: str
    body: str
    hashtags: List[str]
```

The LLM is configured to return output conforming to this schema.

This prevents the content-generation node from returning an arbitrary text response.

---

### `tools/`

Contains the Tavily search integration.

The search tool:

* accepts a search query
* performs an advanced Tavily search
* retrieves up to five results
* returns the search results to the research node

The Tavily API key is loaded from an environment variable:

```text
TAVILY_API_KEY
```

---

### `workflows/`

Contains the LangGraph workflow definition and state.

The workflow consists of two nodes:

```text
research
   ↓
content
```

The workflow starts with the research node and finishes after the content node generates the LinkedIn post.

---

## Workflow State

The workflow uses a typed state object:

```python
class MarketingState(TypedDict):
    topic: str
    research: list
    content: dict
```

This state is passed between the LangGraph nodes.

Conceptually:

```text
Initial State
    │
    │ topic
    ▼
Research Node
    │
    │ + research
    ▼
Content Node
    │
    │ + content
    ▼
Final State
```

---

## Example

The application can be started with a topic such as:

```python
response = app.invoke({
    "topic": "AI Agents in Marketing"
})
```

The system then performs:

```text
"AI Agents in Marketing"
          │
          ▼
 Tavily searches for:
 "Latest trends in AI Agents in Marketing"
          │
          ▼
      Research
          │
          ▼
 Llama 3.1 8B receives:
    - Topic
    - Research
          │
          ▼
   LinkedInPost
```

The final structured result contains:

```text
Title
Hook
Body
Hashtags
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Aditya-Johorey/LinkedIn-Content-Research-Generation-Agent.git

cd LinkedIn-Content-Research-Generation-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Ollama Setup

Install Ollama and make sure it is running locally.

Pull the Llama model:

```bash
ollama pull llama3.1:8b
```

The application currently expects:

```text
llama3.1:8b
```

For embeddings, pull:

```bash
ollama pull nomic-embed-text
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key
```

The Tavily search tool loads this variable using `python-dotenv`.

---

## Running the Application

Once the dependencies and Ollama model are configured:

```bash
python main.py
```

The current example in `main.py` runs the workflow for:

```text
AI Agents in Marketing
```

The generated content is printed to the terminal.

---

## Design Decisions

### Separate Research and Generation

Research and content generation are implemented as separate LangGraph nodes.

This makes the workflow easier to extend than putting the entire process into a single LLM call.

```text
Research
   ↓
Content Generation
```

Additional stages can be added later, such as:

```text
Research
   ↓
Fact Checking
   ↓
Content Generation
   ↓
Quality Evaluation
   ↓
Final Post
```

### Local LLM Inference

The project uses Ollama with Llama 3.1 8B instead of depending entirely on a hosted LLM API.

This allows the application to experiment with:

* local inference
* open-source models
* reduced dependence on external LLM APIs
* local development and experimentation

### Structured Generation

Instead of relying on the model to return a particular text format through prompting alone, the content agent uses a Pydantic schema:

```text
LinkedInPost
├── title
├── hook
├── body
└── hashtags
```

This gives downstream application code a predictable structure.

---

## Current Limitations

The current implementation is intentionally modular but still relatively lightweight.

The ChromaDB and embedding components are initialized as infrastructure, but the current marketing workflow does not yet perform a retrieval step from the Chroma collection before generating the post.

Similarly, the current workflow is:

```text
Research → Content
```

rather than a larger production pipeline containing validation, revision, evaluation, or publishing stages.

These provide natural directions for future development.

---

## Future Improvements

Possible extensions include:

* Add RAG over previously generated LinkedIn posts
* Store successful posts in ChromaDB
* Retrieve relevant historical posts during generation
* Add a content-quality evaluation node
* Add fact-checking after web research
* Add a revision/refinement loop
* Add LinkedIn-specific engagement analysis
* Add audience/persona configuration
* Add tone/style controls
* Add multiple content-generation strategies
* Expose the workflow through a FastAPI API
* Add asynchronous/background execution
* Add persistent workflow memory
* Add automated publishing

A more advanced version could evolve into:

```text
                 Topic
                   │
                   ▼
              Research
                   │
                   ▼
              RAG Search
                   │
                   ▼
          Content Generation
                   │
                   ▼
             Evaluation
                   │
             ┌─────┴─────┐
             │           │
          Pass          Fail
             │           │
             ▼           ▼
          Output      Refinement
                         │
                         └──────→ Evaluation
```

---

## Project Purpose

This project demonstrates how an LLM application can move beyond a single prompt and API call into a modular **agentic workflow**.

The main concepts demonstrated are:

* LangGraph stateful workflows
* Agent/node separation
* External tool integration
* Web research
* Local LLM inference
* Structured LLM outputs
* Vector-store infrastructure
* Modular AI application architecture

---

## License

This project is intended for educational and experimental purposes.
