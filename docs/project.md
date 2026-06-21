# Project: AI Knowledge Assistant Platform

Imagine you're building an internal ChatGPT for a company.

It has:

* FastAPI
* LangGraph
* Multiple workflows
* Mock LLMs
* Mock Vector DB
* Mock SQL DB
* Mock external APIs
* User sessions
* Conversation history
* Telemetry everywhere

The entire project can stay under ~1000 lines of Python, but it will feel like a real production system.

---

# Architecture

```text
                FastAPI

      /chat
      /search
      /summarize
      /analytics
      /feedback

                │

        Middleware
(Request Context Creation)

                │

        Request Context
(trace id isn't enough)

        user_id
        session_id
        conversation_id
        request_id
        experiment_id

                │

        LangGraph Workflow

      Planner
          │
 ┌────────┴────────┐
 │                 │
Retriever      Calculator
 │                 │
VectorDB      External API
 │
Mock LLM

                │

        Response
```

---

# FastAPI Endpoints

## 1. `/chat`

The normal chatbot.

Workflow:

```text
Validate request

↓

Create conversation

↓

Planner

↓

Retriever

↓

LLM

↓

Response
```

---

## 2. `/summarize`

Different workflow.

```text
Load document

↓

Chunk

↓

Summarize

↓

Store summary
```

Now you have multiple traces with different structures.

---

## 3. `/search`

No LLM.

```text
Search

↓

Ranking

↓

Response
```

Useful for seeing traces without LLM spans.

---

## 4. `/analytics`

Returns

* average latency
* requests today
* failed requests

Now you'll naturally think about metrics.

---

## 5. `/feedback`

Stores

```text
thumbs up

thumbs down
```

Later correlate

```text
feedback

↓

trace
```

Very realistic.

---

# LangGraph Workflows

Don't make just one.

---

## Workflow A

Normal RAG

```text
Planner

↓

Retriever

↓

LLM
```

---

## Workflow B

Agent

```text
Planner

↓

Should I use a tool?

↓

Calculator

↓

LLM
```

---

## Workflow C

Document pipeline

```text
Load

↓

Chunk

↓

Embed

↓

Store
```

---

# Mock Components

Don't call real services initially.

---

## Mock LLM

```python
await asyncio.sleep(random.uniform(0.3,1.5))
```

Randomly

* timeout
* hallucinate
* succeed

---

## Mock Vector DB

Randomly

```text
0 documents

3 documents

10 documents
```

---

## Mock SQL

Simulate

```text
50ms

500ms

2 seconds
```

Now latency becomes interesting.

---

## Mock External API

Sometimes

```text
200

404

500

Timeout
```

Perfect for tracing failures.

---

# Context

This is where you'll learn the most.

Every request creates

```python
RequestContext

user_id

session_id

conversation_id

request_id

tenant_id

experiment_id

model_version
```

Store it using

```python
contextvars
```

Never pass it manually.

Every span should automatically receive

```text
user.id

session.id

conversation.id

tenant.id

experiment.id
```

Now you'll understand context propagation.

---

# Trace hierarchy

Your traces should look like

```text
GET /chat

    Authenticate

    Create Session

    Planner

        Retrieve Documents

            Vector DB

        Rank Documents

        Call LLM

    Store History

    Return Response
```

That's a beautiful trace.

---

# Interesting failures

Randomly inject failures.

Maybe

```text
10%

Retriever timeout
```

or

```text
20%

LLM timeout
```

Now ask

> Can I find all failed requests?

Telemetry becomes useful.

---

# Logs

Correlate logs with traces.

Every log automatically contains

```text
trace_id

user_id

conversation_id
```

Now clicking a trace explains the logs.

---

# Metrics

Collect things like

```text
LLM latency

Retriever latency

Average documents retrieved

Failed requests

Tokens

Cost

Tool usage
```

---

# Multiple exporters

Run

```text
Console

↓

Arize
```

simultaneously.

Later maybe

```text
Console

↓

OTLP

↓

Jaeger
```

---

# Span processors

Write your own.

Example

```text
PrivacyProcessor
```

Removes

```text
password

credit card

email
```

before exporting.

Another

```text
CostProcessor
```

Adds

```text
estimated_cost
```

to every LLM span.

Now you'll understand processors.

---

# Sampling

Eventually

```text
Only trace

10%

of successful requests

100%

of failed requests
```

Huge production concept.

---

# Authentication

Users

```text
Alice

Bob

Charlie
```

Each has

```text
user.id
```

Can you filter traces by Alice?

---

# Multiple conversations

Alice

Conversation A

Conversation B

Conversation C

Every request has

```text
conversation.id
```

Now you understand why context matters.

---

# Bonus: Background jobs

Add

```text
POST /ingest
```

Returns immediately.

Starts

```text
Background Task

↓

Chunk

↓

Embed

↓

Store
```

Learn

* trace continuation
* links
* async context

---

# Folder structure

```text
app/

    api/

        chat.py

        search.py

        summarize.py

    workflows/

        rag.py

        summarize.py

        agent.py

    llm/

        mock_llm.py

    db/

        vector_db.py

        sql.py

    telemetry/

        provider.py

        context.py

        processors.py

        exporters.py

    middleware/

        request_context.py

    models/

        request.py

        response.py
```

---

# Telemetry concepts you'll naturally cover

By the end of this project, you'll have touched nearly every important concept in modern observability:

| Concept                      | Where you'll use it                          |
| ---------------------------- | -------------------------------------------- |
| TracerProvider               | Application startup                          |
| Tracer                       | Every module                                 |
| Span                         | Every meaningful operation                   |
| Parent/Child spans           | LangGraph workflows                          |
| Context propagation          | Request middleware, async workflows          |
| Resource                     | Service metadata                             |
| Attributes                   | User, session, conversation, LLM metadata    |
| Events                       | Retries, planner decisions, tool invocations |
| Exceptions                   | Mock failures                                |
| SpanProcessor                | Redaction, cost estimation                   |
| Exporter                     | Console + Arize                              |
| Sampling                     | High-traffic simulation                      |
| Correlation IDs              | Logs ↔ traces                                |
| OpenInference                | LLM, retriever, tool spans                   |
| Distributed tracing concepts | Background jobs and trace links              |

---

## One extra feature I'd add

I'd also build a **Telemetry Playground** endpoint, something like:

```text
POST /debug/run
```

where you can specify:

```json
{
  "user_id": "alice",
  "conversation_id": "conv-42",
  "workflow": "rag",
  "inject_failure": "retriever_timeout",
  "llm_latency_ms": 1500,
  "retrieved_docs": 0
}
```

This lets you deliberately generate interesting traces: slow LLMs, failed tools, empty retrievals, retries, and successful runs. It's like having a simulator for observability. Instead of waiting for production to teach you why telemetry matters, you can create those scenarios on demand and immediately inspect how they appear in Arize. That kind of experimentation is one of the fastest ways to become comfortable with tracing in GenAI applications.
