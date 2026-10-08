from forge.tools.registry import ToolPermission, ToolRegistry, ToolSpec


def noop():
    return None


def test_permission_filter():
    r = ToolRegistry()
    r.register(ToolSpec(name="read", domain="code", description="r", fn=noop))
    r.register(
        ToolSpec(
            name="write",
            domain="code",
            description="w",
            fn=noop,
            permission=ToolPermission.SIDE_EFFECT,
        )
    )
    assert [x.name for x in r.exposed()] == ["read"]
    assert {x.name for x in r.exposed(allow_side_effects=True)} == {"read", "write"}
