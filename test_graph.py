from nodes import route


def test_route_joke():
    assert route({"classification": "joke"}) == "joke"


def test_route_story():
    assert route({"classification": "story"}) == "story"
