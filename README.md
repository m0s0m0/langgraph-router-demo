# LangGraph Router Demo

A minimal LangGraph agent: given a topic, a classifier node decides whether it's a better fit for a joke or a short story, then routes to the matching node via a conditional edge.

```
        START
          │
      classify  ──▶  (LLM decides: "joke" or "story")
       ╱      ╲
   joke        story
     │            │
     └────▶ END ◀─┘
```

## Tech stack
Python, LangGraph 1.2, LangChain (`ChatOpenAI`), pytest.

## Why a graph for a two-way branch

Honestly, a plain `if/else` would do the same job for exactly this example — the value isn't in this toy's complexity, it's in the pattern. The classify→route→branch shape is the same one you'd use for a graph with ten branches, parallel fan-out, retries on individual nodes, or a persisted checkpoint you can resume from — none of which compose cleanly with nested `if` statements, but all of which are one more node/edge away from this exact structure. This repo is the smallest version of that shape, not a claim that it needed LangGraph to exist.

## How it works

- `state.py` — the shared state every node reads/writes: `topic` in, `classification` set by the router, `result` set by whichever branch ran.
- `nodes.py` — `classify_topic` asks the model for exactly one word (`joke`/`story`); `write_joke`/`write_story` generate the actual output; `route` is the plain function LangGraph calls to decide which edge to take based on the state `classify_topic` just set.
- `graph.py` — wires it: `START → classify`, a conditional edge off `classify` keyed by `route`'s return value, then `joke → END` / `story → END`.

The LLM client is built lazily (`get_llm()`, first call only) — so you can import and inspect the compiled graph with zero API key set; you only need one the moment a node actually runs.

## Running it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python3 main.py "a programmer who only codes at 3am"
```

```bash
pytest   # the routing logic itself is pure and deterministic - tested without touching the LLM
```
