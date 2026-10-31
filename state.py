from typing import Literal, TypedDict


class RouterState(TypedDict):
    topic: str
    classification: Literal["joke", "story"]
    result: str
