from langchain_openai import ChatOpenAI

from state import RouterState

_llm = None


def get_llm():
    # lazy - so importing/compiling the graph never requires an API key, only actually calling it does
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return _llm


def classify_topic(state: RouterState) -> dict:
    # a one-word decision - reply with exactly "joke" or "story", nothing else
    prompt = (
        f'Topic: "{state["topic"]}"\n'
        'Would this topic make a better joke or a better short story? '
        'Reply with exactly one word: joke or story.'
    )
    reply = get_llm().invoke(prompt).content.strip().lower()
    classification = "joke" if "joke" in reply else "story"
    return {"classification": classification}


def write_joke(state: RouterState) -> dict:
    prompt = f'Write a short, genuinely funny joke about: {state["topic"]}'
    return {"result": get_llm().invoke(prompt).content}


def write_story(state: RouterState) -> dict:
    prompt = f'Write a short story (3-4 paragraphs) about: {state["topic"]}'
    return {"result": get_llm().invoke(prompt).content}


def route(state: RouterState) -> str:
    return state["classification"]
