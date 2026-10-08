from forge.routing.router import Route, heuristic_route


def test_short_query_routes_direct():
    assert heuristic_route("2+2?").route == Route.DIRECT


def test_large_context_routes_rlm():
    assert heuristic_route("analyze this", context_chars=100_000).route == Route.RLM


def test_memory_intent_routes_memory():
    assert (
        heuristic_route("what did we learn from the previous experiment?").route == Route.RLM_MEMORY
    )
