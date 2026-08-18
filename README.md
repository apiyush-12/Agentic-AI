# LangChain v1.3.14 Learning & Reference Repository

A comprehensive learning repository demonstrating **LangChain v1.3.14** concepts, integrations, and best practices through interactive Jupyter notebooks.

> **Note:** This repository focuses on LangChain v1.x APIs. If you're using v0.x, refer to the [LangChain v0 documentation](https://python.langchain.com/v0.1/).

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Notebooks Guide](#notebooks-guide)
- [Agent Teams](#-agent-teams)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Key Concepts](#key-concepts)
- [Claude Code Agent View](#-claude-code-agent-view)
- [Dependencies & Integrations](#dependencies--integrations)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

---

## 🎯 Overview

This repository is a **hands-on learning resource** for understanding and working with LangChain v1.3.14. It covers foundational concepts through advanced patterns, with working code examples you can run, modify, and experiment with.

**Perfect for:**
- Learning LangChain fundamentals
- Understanding agent-based architectures
- Exploring LLM integrations
- Building retrieval-augmented generation (RAG) systems
- Implementing tool-use and structured outputs

---

## ✨ Features

- 📓 **8 Interactive Jupyter Notebooks** with complete, runnable examples
- 🤖 **Agent Patterns** — from simple tool-calling to complex multi-step reasoning
- 👥 **Agent Teams** — Multi-agent architectures, orchestration, and collaboration
- 🔌 **Multi-Provider Support** — OpenAI, Groq, Mistral AI, Google GenAI
- 🛠️ **Tool Integration** — Define and use custom tools with agents
- 📊 **Structured Output** — Generate validated, typed responses from LLMs
- 🔄 **RAG Implementation** — Vector search and document retrieval patterns
- 📨 **Message Handling** — Human/AI message workflows and conversation management
- 🎯 **Production Patterns** — Middleware, error handling, token management

---

## 📦 Prerequisites

- **Python** 3.11 or 3.14+
- **uv** package manager (fast Python package installer)
- **Jupyter** (for running notebooks)
- **API Keys** for LLM providers (OpenAI, Groq, Mistral, Google GenAI)

### System Requirements

- Windows, macOS, or Linux
- 2GB RAM minimum (4GB+ recommended)
- Internet connection for API calls

---

## 🚀 Installation

### 1. Clone or Download Repository

```bash
cd A:\langchainupdated
```

### 2. Install Dependencies

Using `uv` (recommended — faster than pip):

```bash
uv sync
```

Or with traditional pip:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with your API keys:

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Groq
GROQ_API_KEY=gsk_...

# Mistral AI
MISTRAL_API_KEY=...

# Google GenAI
GOOGLE_API_KEY=...

# Optional: Set default LLM provider
LLM_PROVIDER=openai
```

### 4. Verify Installation

```bash
python -m langchainupdated
```

Expected output:
```
Hello from langchainupdated!
```

---

## 🏃 Quick Start

### Run the Main Entry Point

```bash
python -m langchainupdated
```

### Launch Jupyter Notebooks

```bash
jupyter notebook updatedlangchain/
```

Then open any notebook in your browser and run cells sequentially.

### Run a Specific Notebook

```bash
jupyter notebook updatedlangchain/1-langchainintro.ipynb
```

---

## 📁 Project Structure

```
A:\langchainupdated\
├── README.md                           # This file
├── CLAUDE.md                           # Claude Code configuration
├── pyproject.toml                      # Project metadata & dependencies
├── requirements.txt                    # Pip dependencies (if needed)
├── uv.lock                             # Dependency lock file
├── .env                                # API keys (create this file)
├── .env.example                        # Template for .env
├── .python-version                     # Python version (3.14+)
│
├── updatedlangchain/                   # Jupyter notebooks
│   ├── 1-langchainintro.ipynb         # Agent basics & tool usage
│   ├── 2-modelintegration.ipynb       # LLM provider integrations
│   ├── 3-tools.ipynb                  # Tool definitions & usage
│   ├── 4-messages.ipynb               # Message handling workflows
│   ├── 5-structuredoutput.ipynb       # Structured outputs from LLMs
│   ├── 6-vectorlessrag.ipynb          # RAG without vector databases
│   ├── 7-middleware.ipynb             # Middleware & request logging
│   └── 8-agent-teams.ipynb            # Multi-agent architectures & collaboration
│
├── __init__.py                         # Package entry point
├── .claude/
│   ├── agents/
│   │   └── code-improver.md           # Custom subagent definition
│   └── settings.local.json            # Claude Code local settings
│
└── .venv/                              # Virtual environment (created by uv)
```

---

## 📚 Notebooks Guide

### **1. LangChain Intro** 
📄 `1-langchainintro.ipynb`

**Topics:**
- What are agents and why they matter
- Basic agent architecture (LLM + Tools + Executor)
- Using the ReAct pattern (Reason → Act → Observe)
- Running your first agent

**Key Code:**
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
```

**Duration:** ~15 min to run  
**Difficulty:** Beginner

---

### **2. Model Integration**
📄 `2-modelintegration.ipynb`

**Topics:**
- Integrating multiple LLM providers (OpenAI, Groq, Mistral, Google)
- Provider-specific configuration
- Switching between models
- Cost and latency comparison
- Token counting and cost estimation

**Supported Models:**
- OpenAI: gpt-4, gpt-4-turbo, gpt-3.5-turbo
- Groq: mixtral-8x7b-32768, llama-70b
- Mistral: mistral-small, mistral-medium, mistral-large
- Google: gemini-1.5-pro, gemini-1.5-flash

**Duration:** ~20 min  
**Difficulty:** Beginner-Intermediate

---

### **3. Tools**
📄 `3-tools.ipynb`

**Topics:**
- Defining custom tools with `@tool` decorator
- Input validation and type hints
- Tool documentation for agents
- Error handling in tool execution
- Tool calling vs. function calling
- Building a tool-based agent

**Example:**
```python
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get current weather for a location"""
    return f"Weather in {location}: Sunny, 72°F"
```

**Duration:** ~20 min  
**Difficulty:** Intermediate

---

### **4. Messages**
📄 `4-messages.ipynb`

**Topics:**
- Message types (HumanMessage, AIMessage, ToolMessage, SystemMessage)
- Building conversation histories
- Message roles and content
- Working with chat history
- Building stateful agents

**Use Cases:**
- Multi-turn conversations
- Conversation memory
- Context building for complex tasks

**Duration:** ~15 min  
**Difficulty:** Beginner-Intermediate

---

### **5. Structured Output**
📄 `5-structuredoutput.ipynb`

**Topics:**
- Enforcing structured output from LLMs
- Using Pydantic models with LangChain
- JSON mode and validation
- Extracting data reliably
- Type-safe LLM responses

**Example:**
```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    email: str

llm_with_structure = llm.with_structured_output(Person)
result = llm_with_structure.invoke("Extract info from text")
```

**Duration:** ~15 min  
**Difficulty:** Intermediate

---

### **6. Vector-less RAG**
📄 `6-vectorlessrag.ipynb`

**Topics:**
- Retrieval-Augmented Generation (RAG) without vector databases
- Document chunking and hierarchy
- Tree-based retrieval
- PDF processing
- Hybrid retrieval strategies

**Use Cases:**
- Document Q&A
- Paper summarization
- Knowledge base search
- Long-context document handling

**Duration:** ~25 min  
**Difficulty:** Intermediate-Advanced

---

### **7. Middleware**
📄 `7-middleware.ipynb`

**Topics:**
- Request/response logging
- Cost tracking
- Token usage monitoring
- Middleware implementation patterns
- Error recovery and retry logic
- Production-ready patterns

**Example:**
```python
from langchain_core.callbacks import CallbackManager

manager = CallbackManager([
    LoggingCallback(),
    CostTrackingCallback(),
    TokenCountingCallback()
])
```

**Duration:** ~20 min  
**Difficulty:** Advanced

---

### **8. Agent Teams**
📄 `8-agent-teams.ipynb`

**Topics:**
- Multi-agent system architectures (Orchestrator, Peer-to-Peer, Hierarchical)
- Agent team coordination and collaboration patterns
- Specialized agent types and their roles
- Building orchestrator-based teams
- Sequential multi-agent workflows
- Tool allocation across agents
- Real-world use cases (customer support, research, business ops)
- State management and communication between agents
- Failure handling and recovery

**Key Concepts:**
- Orchestrator Pattern — Central coordination
- Peer-to-Peer Pattern — Direct communication
- Hierarchical Pattern — Multi-layer structure
- Common agent types: Researcher, Analyzer, Executor, Reviewer, Memory, Safety

**Code Examples:**
- Simple orchestrator delegating to specialized agents
- Financial analysis team (market → sentiment → report)
- Complex workflow with research, validation, memory, and safety agents

**Frameworks Covered:**
- LangGraph (native LangChain solution)
- AutoGen (Microsoft's framework)
- CrewAI (role-based collaboration)

**Duration:** ~30 min to run all examples  
**Difficulty:** Intermediate-Advanced

---

## 👥 Agent Teams Summary

**Agent Teams** enable multi-agent systems where specialized agents collaborate to solve complex problems. Each agent handles specific domains, enabling parallelization, better scalability, and real-world problem simulation.

### Why Agent Teams?

- ✅ **Specialization** — Each agent handles specific expertise
- ✅ **Parallelization** — Multiple agents work concurrently
- ✅ **Scalability** — Add agents for larger problems
- ✅ **Resilience** — Isolated agents prevent cascading failures
- ✅ **Maintainability** — Clear roles and separation of concerns

### Architecture Patterns

1. **Orchestrator Pattern** — Central agent delegates to specialists
2. **Peer-to-Peer Pattern** — Agents communicate directly
3. **Hierarchical Pattern** — Multi-layer agent structure

### Common Agent Types

| Type | Role |
|------|------|
| **Orchestrator** | Coordinates workflow & delegates tasks |
| **Researcher** | Gathers and analyzes information |
| **Analyzer** | Processes and interprets data |
| **Executor** | Performs actions in the world |
| **Reviewer** | Validates results and quality |
| **Memory** | Manages knowledge and context |
| **Safety** | Monitors and enforces constraints |

### Use Cases

- **Customer Support** — Triage → Knowledge → Resolution → Escalation
- **Research** — Literature search → Data processing → Writing → Review
- **Business Ops** — Demand forecasting → Inventory → Logistics → Finance

### Next Steps

👉 **See Notebook 8** (`8-agent-teams.ipynb`) for:
- Complete code examples and implementations
- Orchestrator pattern walkthrough
- Multi-agent collaboration workflows
- Specialized agent team examples
- Framework comparisons (LangGraph, AutoGen, CrewAI)

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
# LLM Provider API Keys
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
MISTRAL_API_KEY=...
GOOGLE_API_KEY=...

# Optional Settings
LLM_PROVIDER=openai              # Default provider
LLM_TEMPERATURE=0.7              # 0-1, lower = more deterministic
LLM_MAX_TOKENS=2000              # Maximum tokens in response
DEBUG=True                        # Enable debug logging
```

### Python Version

The project requires Python 3.11+. Check your version:

```bash
python --version
```

If needed, install the correct version from [python.org](https://www.python.org/) or use `pyenv`/`nvm`.

### Package Manager Configuration

The project uses `uv` with the `uv_build` backend. See `pyproject.toml` for full configuration.

---

## 💡 Usage Examples

### Run a Simple Agent

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

llm = ChatOpenAI(model="gpt-4")
agent = create_tool_calling_agent(llm, [add], prompt)
executor = AgentExecutor(agent=agent, tools=[add])

result = executor.invoke({"input": "What is 5 + 3?"})
print(result["output"])  # "8"
```

### Use Multiple Providers

```python
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI

# Switch between providers
openai = ChatOpenAI(model="gpt-4")
groq = ChatGroq(model="mixtral-8x7b-32768")
mistral = ChatMistralAI(model="mistral-large")

# Use any of them interchangeably
response = openai.invoke("What is LangChain?")
```

### Extract Structured Data

```python
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

class Company(BaseModel):
    name: str
    founded: int
    ceo: str

llm = ChatOpenAI(model="gpt-4")
llm_structured = llm.with_structured_output(Company)

company = llm_structured.invoke("Tell me about Anthropic")
print(company.name)  # "Anthropic"
```

---

## 🧠 Key Concepts

### Agents
Autonomous systems that use an LLM to decide which actions to take. An agent has:
- **Reasoning**: LLM decides what to do next
- **Tools**: Functions the agent can call
- **Loop**: Repeats until goal is reached

### Agent Teams
Multiple agents working together to solve complex problems. Agent teams provide:
- **Specialization** — Each agent handles specific domains
- **Parallelization** — Multiple agents work on different tasks simultaneously
- **Coordination** — Central orchestrator or peer-to-peer communication
- **Scalability** — Add more agents as complexity grows
- **Resilience** — Isolation between agents prevents cascading failures

**Architectures:**
1. **Orchestrator Pattern** — One agent coordinates others
2. **Peer-to-Peer Pattern** — Agents communicate directly
3. **Hierarchical Pattern** — Multiple layers of agents

### Tools
Functions that agents can call. Defined with:
- Name and description (for agent to understand)
- Input schema (what parameters it takes)
- Implementation (the actual function)

### Message Types
- **HumanMessage**: Input from the user
- **AIMessage**: Response from the LLM
- **ToolMessage**: Result from a tool call
- **SystemMessage**: Instructions for the LLM

### Structured Output
Enforcing LLM responses to match a schema (Pydantic model). Ensures:
- Valid JSON structure
- Type correctness
- Required fields presence

### RAG (Retrieval-Augmented Generation)
Combining retrieved documents with LLM generation:
1. **Retrieve** relevant documents
2. **Augment** the prompt with context
3. **Generate** response using LLM

---

## 🔍 Claude Code Agent View

Claude Code provides a powerful **Agent View** feature that enables real-time visualization and monitoring of agent execution, state management, and debugging workflows. This section details how to leverage this tool when developing and testing LangChain agents.

### What is Agent View?

The **Agent View** is an integrated panel in Claude Code that displays detailed information about agent execution, including:
- **Agent execution timeline** — Step-by-step breakdown of what the agent is doing
- **Tool invocations** — Which tools the agent called and their inputs/outputs
- **State tracking** — Current state and memory of the agent
- **Error logs** — Any errors or warnings that occurred
- **Performance metrics** — Execution time, token usage, costs
- **Message history** — Full conversation context between user and agent

### Why Use Agent View?

Agent View solves critical challenges in agent development:

1. **Debugging Complexity** — Understand why agents make certain decisions
2. **Tool Verification** — Confirm tools are being called correctly with proper arguments
3. **Loop Tracking** — Monitor multi-step reasoning loops (ReAct pattern)
4. **Error Diagnosis** — Identify failures in tool execution or LLM reasoning
5. **Performance Optimization** — Track token usage and API costs per request
6. **Quality Assurance** — Verify agents behave correctly across different inputs

### Accessing Agent View

#### In Claude Code CLI

When running agents with Claude Code, the Agent View appears automatically:

```bash
claude code --workspace .
# Then run your agent code
```

The view updates in real-time as the agent executes.

#### In Claude Code Web (claude.ai/code)

1. Open [claude.ai/code](https://claude.ai/code)
2. Create or open a project with agent code
3. Run your agent with the **▶️ Run** button
4. Click the **Agent View** tab to see execution details

#### In IDE Extensions (VS Code, JetBrains)

When running agents through Claude Code IDE extensions:

1. Run your agent code
2. Look for the **Agent Execution** panel in the IDE
3. Expand to see detailed agent steps and tool calls

### Agent View Features

#### 1. **Execution Timeline**

Shows the chronological sequence of agent steps:

```
Step 1: Initial Reasoning
├─ Model: GPT-4
├─ Temperature: 0.7
└─ Input: "What is the weather in New York?"

Step 2: Tool Selection
├─ Selected Tool: get_weather
├─ Arguments: {"location": "New York"}
└─ Status: Running...

Step 3: Tool Execution
├─ Result: "Sunny, 72°F, humidity 65%"
├─ Execution Time: 245ms
└─ Status: Success

Step 4: Response Generation
├─ Model: GPT-4
├─ Final Output: "The weather in New York is currently sunny..."
└─ Status: Complete
```

#### 2. **Tool Call Inspector**

Detailed view of each tool invocation:

```json
{
  "tool_name": "get_weather",
  "arguments": {
    "location": "New York",
    "units": "fahrenheit"
  },
  "execution_time_ms": 245,
  "result": {
    "temperature": 72,
    "condition": "sunny",
    "humidity": 65
  },
  "status": "success"
}
```

#### 3. **State & Memory Tracking**

Monitor agent internal state:

```python
# Agent State View
{
  "conversation_history": [
    {"role": "user", "content": "What's the weather?"},
    {"role": "assistant", "content": "I'll check that for you..."}
  ],
  "tools_available": ["get_weather", "get_forecast"],
  "current_step": 4,
  "total_steps": 5,
  "memory": {
    "queries": ["weather"],
    "results": [...]
  }
}
```

#### 4. **Error & Warning Logs**

Real-time error reporting:

```
⚠️ Warning: Tool 'get_weather' took 2.3s (slower than usual)
❌ Error: Invalid argument "units" for get_weather
📋 Info: Retrying with corrected arguments...
✅ Success: Tool call succeeded on retry
```

#### 5. **Performance Metrics**

Token usage and cost tracking:

```
Total Tokens Used: 1,247
├─ Input Tokens: 850
├─ Output Tokens: 397
│
Total API Cost: $0.024
├─ Model: GPT-4 (0.03/1K input, 0.06/1K output)
│
Execution Time: 2.3 seconds
└─ Tool Calls: 2 requests (avg 245ms each)
```

### Using Agent View in Development

#### Example Workflow: Debugging a Misbehaving Agent

**Scenario:** Your agent is calling the wrong tool or using incorrect arguments.

1. **Run your agent** with test input
2. **Open Agent View**
3. **Inspect the execution timeline** — locate where it went wrong
4. **Check tool arguments** — verify the model is generating correct parameters
5. **Review error logs** — see what the error message was
6. **Fix the issue** — update your tool definition or prompt
7. **Re-run and verify** — confirm the fix works

**Example Issue Detected:**

```
Step 2: Tool Selection
❌ Selected Tool: calculate (incorrect)
   Intended Tool: get_weather
   
   Problem: Model confused "weather" with math calculation
   
   Solution: Improve tool descriptions in agent setup
```

#### Example: Optimizing Agent Performance

Use Agent View to identify bottlenecks:

```
Execution Time Breakdown:
├─ LLM Reasoning: 850ms ✓ Normal
├─ Tool Call #1: 2300ms ⚠️ Slow
├─ Tool Call #2: 180ms ✓ Normal
└─ Final Response: 200ms ✓ Normal

Recommendation: Optimize get_weather tool (2.3s is slow)
```

### Agent View in Testing

Use Agent View when writing tests for agents:

```python
def test_agent_weather_query():
    agent = create_agent()
    
    # Run agent (Agent View appears)
    result = agent.invoke({"input": "What's the weather?"})
    
    # In Agent View, verify:
    # ✓ Correct tool was selected
    # ✓ Arguments were formatted properly
    # ✓ Tool executed successfully
    # ✓ Final output was accurate
    # ✓ No errors in execution
    
    assert "sunny" in result["output"].lower()
```

### Best Practices with Agent View

#### 1. **Monitor First Runs**
When you first deploy an agent, keep Agent View open to catch any issues.

#### 2. **Use for Troubleshooting**
Before diving into code, check Agent View to understand the failure.

#### 3. **Compare Tool Behavior**
Run the same query with different tools/models and compare their execution paths.

#### 4. **Track Performance Over Time**
Document execution times and costs to identify performance regressions.

#### 5. **Share with Teammates**
Screenshot or export Agent View logs for team discussion and debugging.

### Agent View with LangChain Agents

When using LangChain agents, Agent View automatically integrates:

```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

# When you run this in Claude Code:
result = executor.invoke({"input": "user question"})
# Agent View automatically captures all steps above ☝️
```

Agent View shows:
- Each LLM call and its reasoning
- Tool selections from the executor
- Tool execution results
- Loop iterations (ReAct reasoning cycles)
- Final output generation

### Exporting & Sharing Agent Traces

Export Agent View data for analysis:

1. **Export as JSON** — Full execution trace
2. **Export as CSV** — Metrics and performance data
3. **Share Link** — Generate a shareable link to the execution trace
4. **Screenshot** — Quick visual reference

### Agent View Settings

Customize Agent View behavior in your Claude Code settings:

```json
{
  "agent": {
    "view": {
      "enabled": true,
      "captureToolCalls": true,
      "captureState": true,
      "captureMetrics": true,
      "maxHistorySteps": 100,
      "autoExpand": ["errors", "warnings"]
    }
  }
}
```

### Limitations & Considerations

- **Privacy:** Agent View captures all inputs/outputs (don't expose sensitive data)
- **Performance:** Detailed logging has minimal overhead (~2-5%)
- **Storage:** Long execution traces consume disk space (export as needed)
- **Real-time Updates:** Works best with latency <5s per step

### Additional Resources on Agent View

- [Claude Code Documentation](https://claude.ai/code)
- [LangChain AgentExecutor Docs](https://python.langchain.com/docs/modules/agents/)
- [Debugging Agents Guide](https://python.langchain.com/docs/debugging)
- [Claude Code Agent View Tutorial](https://claude.ai/code/help/agent-view)

---

## 🔌 Dependencies & Integrations

### Core LangChain Packages

| Package | Purpose | Version |
|---------|---------|---------|
| `langchain-core` | Core LangChain abstractions | Latest |
| `langchain` | Main LangChain package | 0.1.x+ |
| `langchain-community` | Community integrations | Latest |

### LLM Provider Integrations

| Provider | Package | Models |
|----------|---------|--------|
| **OpenAI** | `langchain-openai` | GPT-4, GPT-3.5-turbo |
| **Groq** | `langchain-groq` | Mixtral, Llama 70B |
| **Mistral AI** | `langchain-mistralai` | Mistral Small/Medium/Large |
| **Google GenAI** | `langchain-google-genai` | Gemini 1.5 Pro/Flash |

### Utilities

| Package | Purpose |
|---------|---------|
| `python-dotenv` | Load `.env` files |
| `pydantic` | Data validation & schemas |
| `requests` | HTTP client |
| `jupyter` | Notebook environment |
| `ipykernel` | Jupyter kernel |

See `pyproject.toml` or `requirements.txt` for complete list.

---

## 🆘 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'langchain'`

**Solution:** Install dependencies:
```bash
uv sync
# or
pip install -r requirements.txt
```

---

### Issue: `API Key not found` or `Invalid API key`

**Solution:** 
1. Create `.env` file in project root
2. Add your API keys:
   ```env
   OPENAI_API_KEY=sk-...
   ```
3. Restart Jupyter kernel

---

### Issue: Jupyter notebook won't start

**Solution:**
```bash
pip install jupyter ipykernel
jupyter notebook
```

---

### Issue: Token limit exceeded

**Solution:**
- Use a model with higher token limit (e.g., GPT-4 instead of GPT-3.5)
- Chunk documents into smaller pieces
- Enable token counting middleware (see notebook 7)

---

### Issue: Slow API responses

**Solution:**
- Use a faster provider (Groq is typically fastest)
- Reduce token limits
- Use streaming for long responses

---

## 📖 Resources

### Official Documentation
- [LangChain Documentation](https://python.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [LangSmith (Debugging & Monitoring)](https://smith.langchain.com/)

### API Documentation
- [OpenAI API](https://platform.openai.com/docs/api-reference)
- [Groq API](https://console.groq.com/docs)
- [Mistral AI API](https://docs.mistral.ai/api/)
- [Google GenAI API](https://ai.google.dev/docs)

### Learning Resources
- [LangChain Docs - Concepts](https://python.langchain.com/docs/concepts/)
- [LangChain Templates](https://github.com/langchain-ai/langchain/tree/master/templates)
- [LangChain YouTube Channel](https://www.youtube.com/@LangChain)

### Related Topics
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Typing](https://docs.python.org/3/library/typing.html)
- [Jupyter Notebooks](https://jupyter.org/)

---

## 🤝 Contributing

This is a learning repository. Feel free to:
- Modify notebooks for experiments
- Add new examples and use cases
- Document findings and best practices
- Report issues or suggestions

---

## 📝 License

Educational use. Refer to individual LangChain packages for their licenses.

---

## ✍️ Author

Created for learning and reference with **LangChain v1.3.14**

**Last Updated:** August 2026  
**Python Version:** 3.11+  
**LangChain Version:** 1.3.14+

---

## 🎓 Next Steps

1. **Start with Notebook 1** — Understand agent fundamentals
2. **Explore Notebook 2** — Try different LLM providers
3. **Build with Notebook 3** — Create custom tools
4. **Learn Notebook 4** — Master message handling
5. **Practice Notebook 5** — Work with structured outputs
6. **Dive into Notebook 6** — Implement RAG patterns
7. **Optimize with Notebook 7** — Add production middleware
8. **Master Notebook 8** — Build multi-agent teams
9. **Experiment** — Modify code, run examples, break things
10. **Integrate** — Use these patterns in your own projects

Happy learning! 🚀
