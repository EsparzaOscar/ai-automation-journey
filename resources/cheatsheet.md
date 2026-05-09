# AI Automation Cheatsheet 🤖
> Quick reference for the 60-day syllabus. Update this as you learn.

---

## Table of Contents
1. [Git Essentials](#1-git-essentials)
2. [Python Quick Reference](#2-python-quick-reference)
3. [Working with APIs](#3-working-with-apis)
4. [Prompt Engineering](#4-prompt-engineering)
5. [OpenAI API](#5-openai-api)
6. [Anthropic Claude API](#6-anthropic-claude-api)
7. [n8n Quick Reference](#7-n8n-quick-reference)
8. [Environment Variables & Security](#8-environment-variables--security)
9. [LangChain Agents](#9-langchain-agents)
10. [CrewAI](#10-crewai)
11. [Useful Terminal Commands](#11-useful-terminal-commands)
12. [VS Code / PyCharm Shortcuts](#12-pycharm-shortcuts)

---

## 1. Git Essentials

```bash
# Daily workflow
git add .                          # Stage all changes
git commit -m "notes: day X — topic"  # Commit with message
git push origin main               # Push to GitHub

# Commit message prefixes (keep history readable)
# feat:    new script or workflow
# notes:   learning notes update
# fix:     bug fix
# resources: added links or references
# refactor: cleaned up existing code

# Useful checks
git status                         # See what's changed
git log --oneline                  # See commit history (compact)
git diff                           # See exact line changes

# Undo mistakes
git restore <file>                 # Discard unsaved changes to a file
git reset --soft HEAD~1            # Undo last commit (keep changes)
```

---

## 2. Python Quick Reference

```python
# --- File I/O ---
with open("file.txt", "r") as f:
    content = f.read()

with open("output.txt", "w") as f:
    f.write("Hello")

# --- JSON ---
import json

with open("data.json", "r") as f:
    data = json.load(f)             # Parse JSON file → dict

json_string = json.dumps(data, indent=2)  # dict → JSON string

# --- List comprehensions ---
doubled = [x * 2 for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]

# --- Error handling ---
try:
    result = risky_function()
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    print("Always runs")

# --- f-strings ---
name = "Claude"
print(f"Hello, {name}!")
print(f"Pi is approximately {3.14159:.2f}")

# --- Useful built-ins ---
enumerate(["a","b","c"])           # → (0,"a"), (1,"b"), (2,"c")
zip([1,2,3], ["a","b","c"])        # → (1,"a"), (2,"b"), (3,"c")
sorted(items, key=lambda x: x["date"], reverse=True)

# --- Virtual environment (terminal) ---
python -m venv venv                # Create venv
source venv/bin/activate           # Activate (Mac/Linux)
venv\Scripts\activate              # Activate (Windows)
pip install package-name           # Install package
pip freeze > requirements.txt      # Save dependencies
pip install -r requirements.txt    # Install from file
```

---

## 3. Working with APIs

```python
import requests

# --- GET request ---
response = requests.get(
    "https://api.example.com/data",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    params={"limit": 10, "page": 1}   # Appended as ?limit=10&page=1
)
response.raise_for_status()           # Raises error if status != 200
data = response.json()                # Parse response body

# --- POST request (send JSON body) ---
response = requests.post(
    "https://api.example.com/items",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={"name": "test", "value": 42}   # Auto-serializes to JSON
)

# --- Common status codes ---
# 200 OK            - success
# 201 Created       - resource created
# 400 Bad Request   - your request has an error
# 401 Unauthorized  - bad or missing API key
# 429 Too Many Req  - rate limited, slow down
# 500 Server Error  - problem on their end

# --- Retry logic (basic) ---
import time

def call_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                time.sleep(2 ** attempt)   # Exponential backoff
            else:
                raise
    raise Exception("Max retries exceeded")
```

---

## 4. Prompt Engineering

### Core Patterns

| Pattern | When to use | Example |
|---|---|---|
| **Zero-shot** | Simple, clear tasks | "Summarize this text:" |
| **Few-shot** | When output format matters | Provide 2–3 input/output examples first |
| **Chain-of-thought** | Complex reasoning | "Think step by step before answering." |
| **Role prompting** | Tone/expertise control | "You are a senior Python developer..." |
| **Output formatting** | Structured data | "Respond only in valid JSON." |

### Prompt Template (Python)

```python
def build_prompt(context: str, task: str, examples: list = None) -> str:
    prompt = f"You are a helpful AI assistant.\n\n"
    if examples:
        prompt += "Examples:\n"
        for ex in examples:
            prompt += f"Input: {ex['input']}\nOutput: {ex['output']}\n\n"
    prompt += f"Context:\n{context}\n\nTask:\n{task}"
    return prompt
```

### Golden Rules
- Be specific — vague prompts get vague outputs
- Tell it the FORMAT you want (JSON, bullet list, paragraph)
- Tell it what NOT to do, not just what to do
- Add "Think step by step" for any multi-step reasoning
- For JSON output: add "Respond only with valid JSON, no extra text"

---

## 5. OpenAI API

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Basic chat completion ---
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",   "content": "Summarize this in 3 bullet points: ..."}
    ],
    max_tokens=500,
    temperature=0.3    # 0 = deterministic, 1 = creative
)
text = response.choices[0].message.content

# --- JSON mode (structured output) ---
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Respond only with valid JSON."},
        {"role": "user",   "content": "Extract name and email from: John Doe, john@example.com"}
    ],
    response_format={"type": "json_object"}
)
import json
data = json.loads(response.choices[0].message.content)

# --- Embeddings (for RAG) ---
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="The text to embed"
)
vector = response.data[0].embedding   # List of floats

# --- Models & rough pricing (check platform.openai.com for current) ---
# gpt-4o          - best quality, multimodal
# gpt-4o-mini     - fast, cheap, great for most tasks
# text-embedding-3-small - embeddings, very cheap
```

---

## 6. Anthropic Claude API

```python
import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# --- Basic message ---
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain RAG in simple terms."}
    ]
)
text = message.content[0].text

# --- System prompt ---
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="You are an expert Python developer. Be concise.",
    messages=[
        {"role": "user", "content": "Review this code: ..."}
    ]
)

# --- Multi-turn conversation ---
history = []

def chat(user_message):
    history.append({"role": "user", "content": user_message})
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=history
    )
    assistant_reply = response.content[0].text
    history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

# --- Models ---
# claude-opus-4-5     - most powerful, best for complex reasoning
# claude-sonnet-4-5   - best balance of speed + quality (default choice)
# claude-haiku-4-5    - fastest, cheapest, great for simple tasks
```

---

## 7. n8n Quick Reference

### Core Concepts
| Term | What it means |
|---|---|
| **Workflow** | The full automation (like a recipe) |
| **Node** | One step in the workflow (trigger, action, logic) |
| **Trigger node** | Starts the workflow (webhook, schedule, email, etc.) |
| **Expression** | Dynamic value using `{{ }}` syntax |
| **Item** | One piece of data flowing through the workflow |

### Useful n8n Expressions
```js
// Access previous node's output
{{ $json.fieldName }}
{{ $json["field with spaces"] }}

// Access a specific node by name
{{ $node["Node Name"].json.fieldName }}

// Current date/time
{{ $now.toISO() }}
{{ $now.format("YYYY-MM-DD") }}

// String operations
{{ $json.name.toUpperCase() }}
{{ $json.email.split("@")[0] }}

// Conditional
{{ $json.status === "active" ? "yes" : "no" }}
```

### Self-hosting n8n (Railway — free tier)
1. Go to railway.app → New Project → Deploy from template → search "n8n"
2. Add env var: `N8N_BASIC_AUTH_ACTIVE=true`, `N8N_BASIC_AUTH_USER`, `N8N_BASIC_AUTH_PASSWORD`
3. Your n8n instance is live at the generated Railway URL

---

## 8. Environment Variables & Security

```python
# --- .env file (never commit this to GitHub!) ---
# Create a file named exactly: .env
# Contents:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# MY_WEBHOOK_SECRET=abc123

# --- Load in Python ---
from dotenv import load_dotenv
import os

load_dotenv()                          # Reads .env into environment
api_key = os.getenv("OPENAI_API_KEY")  # Retrieve value safely

# Install: pip install python-dotenv

# --- .gitignore (add this to your project root) ---
# Create a file named: .gitignore
# Contents:
# .env
# venv/
# __pycache__/
# *.pyc
# .DS_Store
```

> ⚠️ Rule: If your API key ever ends up on GitHub, rotate it immediately on the provider's dashboard.

---

## 9. LangChain Agents

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain import hub

# --- Setup ---
llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [DuckDuckGoSearchRun()]

# Pull a standard ReAct prompt from LangChain Hub
prompt = hub.pull("hwchase17/react")

# --- Create and run agent ---
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({
    "input": "What is the current price of Bitcoin?"
})
print(result["output"])

# --- Add memory ---
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# Pass memory= to AgentExecutor

# Install: pip install langchain langchain-openai langchain-community duckduckgo-search
```

---

## 10. CrewAI

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

# --- Define Agents ---
researcher = Agent(
    role="Research Analyst",
    goal="Find accurate and relevant information on the given topic",
    backstory="You are an expert researcher with a talent for finding reliable sources.",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write clear, concise summaries from research findings",
    backstory="You are a skilled writer who turns complex research into readable content.",
    llm=llm,
    verbose=True
)

# --- Define Tasks ---
research_task = Task(
    description="Research the latest trends in {topic}. Find key facts, statistics, and examples.",
    expected_output="A bullet-point list of 5–7 key findings with sources.",
    agent=researcher
)

write_task = Task(
    description="Using the research findings, write a 3-paragraph summary about {topic}.",
    expected_output="A well-structured 3-paragraph summary in plain English.",
    agent=writer
)

# --- Assemble Crew ---
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,   # Tasks run in order
    verbose=True
)

result = crew.kickoff(inputs={"topic": "AI automation tools in 2025"})
print(result)

# Install: pip install crewai langchain-openai
```

---

## 11. Useful Terminal Commands

```bash
# Python
python --version
python script.py
pip install package
pip list                           # Show installed packages
pip show package                   # Show package details

# Files & folders
ls -la                             # List all files (Mac/Linux)
dir                                # List files (Windows)
mkdir folder-name                  # Create folder
rm filename                        # Delete file (careful!)
cat filename                       # Print file contents

# Process management
Ctrl+C                             # Stop a running script
Ctrl+Z                             # Suspend (then kill with: kill %1)

# Networking
curl https://api.example.com       # Quick API test in terminal
```

---

## 12. PyCharm Shortcuts

| Action | Windows/Linux | Mac |
|---|---|---|
| Commit changes | `Ctrl+K` | `Cmd+K` |
| Push to GitHub | `Ctrl+Shift+K` | `Cmd+Shift+K` |
| Open terminal | `Alt+F12` | `Option+F12` |
| Find in file | `Ctrl+F` | `Cmd+F` |
| Find in project | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Run file | `Shift+F10` | `Ctrl+R` |
| Comment line | `Ctrl+/` | `Cmd+/` |
| Duplicate line | `Ctrl+D` | `Cmd+D` |
| Move line up/down | `Shift+Alt+↑↓` | `Shift+Option+↑↓` |
| Reformat code | `Ctrl+Alt+L` | `Cmd+Option+L` |
| Open file quickly | `Ctrl+Shift+N` | `Cmd+Shift+O` |
| Multi-cursor | `Alt+Click` | `Option+Click` |

---

*Last updated: Day 1 — keep adding to this as you discover useful patterns.*
