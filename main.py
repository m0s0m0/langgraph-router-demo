import sys

from graph import build_graph


def main():
    topic = " ".join(sys.argv[1:]) or "a cat who thinks it's a dog"
    app = build_graph()
    result = app.invoke({"topic": topic})
    print(f'topic: {topic}')
    print(f'routed to: {result["classification"]}')
    print()
    print(result["result"])


if __name__ == "__main__":
    main()
