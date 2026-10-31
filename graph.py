from langgraph.graph import END, START, StateGraph

from nodes import classify_topic, route, write_joke, write_story
from state import RouterState


def build_graph():
    graph = StateGraph(RouterState)

    graph.add_node("classify", classify_topic)
    graph.add_node("joke", write_joke)
    graph.add_node("story", write_story)

    graph.add_edge(START, "classify")
    graph.add_conditional_edges("classify", route, {"joke": "joke", "story": "story"})
    graph.add_edge("joke", END)
    graph.add_edge("story", END)

    return graph.compile()
