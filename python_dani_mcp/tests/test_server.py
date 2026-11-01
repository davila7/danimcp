"""Server tests against a mocked upstream API (no network)."""

from __future__ import annotations

import json
import re

import httpx2
import pytest
from fastmcp import Client

from api import DaniAPI
from server import create_server
from views import SHARED_FILES, VIEWS

UI_MIME = "text/html;profile=mcp-app"

FIXTURES = {
    "hello": {"message": "Hi"},
    "about_me": {"name": "Daniel Ávila Arias", "occupation": "AI Software Engineer"},
    "technologies": [{"name": "Python", "level": "Advanced"}, {"name": "bitbucket", "Level": "Intermediate"}],
    "projects": [{"id": 1, "title": "AI Templates", "des": "Templates", "link": "https://aitmpl.com"}],
    "talks": {"title": "Speaker"},
    "skills": {
        "programming": {"languages": ["JavaScript/TypeScript", "Python", "Java"]},
        "ai_llm_tools": ["LangChain"],
    },
}


class Upstream:
    """Mock of danielavila.me/api that records requests."""

    def __init__(self) -> None:
        self.requests: list[httpx2.Request] = []

    def __call__(self, request: httpx2.Request) -> httpx2.Response:
        self.requests.append(request)
        endpoint = request.url.path.removeprefix("/api/")
        assert request.headers["user-agent"].startswith("DaniMCP/")  # Cloudflare blocks requests without it
        if request.method == "POST" and endpoint == "contact":
            return httpx2.Response(200, json={"ok": True, "received": json.loads(request.content)})
        if endpoint in FIXTURES:
            return httpx2.Response(200, json=FIXTURES[endpoint])
        return httpx2.Response(500, text="<html>500</html>")


@pytest.fixture
def upstream() -> Upstream:
    return Upstream()


@pytest.fixture
async def client(upstream: Upstream):
    api = DaniAPI("https://example.test/api", transport=httpx2.MockTransport(upstream))
    async with Client(create_server(api)) as c:
        yield c


async def test_lists_all_tools_with_annotations(client: Client):
    tools = {t.name: t for t in await client.list_tools()}
    assert set(tools) == {
        "hello",
        "about_me",
        "technologies",
        "projects",
        "contact",
        "send_contact_message",
        "talks",
        "skills",
        "check_skill",
    }
    for name, tool in tools.items():
        assert tool.output_schema is None, name  # see note in tools.py
        assert tool.annotations.read_only_hint is (name != "send_contact_message"), name


async def test_ui_tools_link_to_registered_views(client: Client):
    tools = {t.name: t for t in await client.list_tools()}
    resources = {str(r.uri): r for r in await client.list_resources()}
    linked = {name: t.meta["ui"]["resourceUri"] for name, t in tools.items() if t.meta and "ui" in t.meta}
    assert linked == {
        "about_me": "ui://danimcp/profile",
        "skills": "ui://danimcp/skills-chart",
        "technologies": "ui://danimcp/tech-chart",
        "projects": "ui://danimcp/projects",
    }
    assert set(linked.values()) == set(resources)


@pytest.mark.parametrize("view", VIEWS.values(), ids=lambda v: v.uri)
async def test_view_resources(client: Client, view):
    [content] = await client.read_resource(view.uri)
    assert content.mime_type == UI_MIME
    assert content.meta["ui"]["csp"]["resourceDomains"] == ["https://cdn.jsdelivr.net"]
    assert content.text.lstrip().startswith("<!DOCTYPE html>")
    for marker in SHARED_FILES:
        assert marker not in content.text
    # Every external script/import must be covered by the declared CSP.
    for url in re.findall(r"https://[^\s\"')]+\.js", content.text):
        assert url.startswith("https://cdn.jsdelivr.net/"), url


async def test_structured_content(client: Client):
    result = await client.call_tool("about_me", {})
    assert result.structured_content == FIXTURES["about_me"]
    assert json.loads(result.content[0].text) == FIXTURES["about_me"]

    result = await client.call_tool("projects", {})
    assert result.structured_content == {"projects": FIXTURES["projects"]}


async def test_technologies_normalizes_level_key(client: Client):
    result = await client.call_tool("technologies", {})
    assert result.structured_content["technologies"][1] == {"name": "bitbucket", "level": "Intermediate"}


@pytest.mark.parametrize(
    ("query", "has_skill", "names"),
    [
        ("python", True, ["Python", "Python"]),
        ("TypeScript", True, ["JavaScript/TypeScript"]),
        ("Java", True, ["Java"]),  # must not match JavaScript
        ("bitbucket", True, ["bitbucket"]),
        ("cobol", False, []),
    ],
)
async def test_check_skill(client: Client, query, has_skill, names):
    result = await client.call_tool("check_skill", {"skill_name": query})
    assert result.structured_content["has_skill"] is has_skill
    assert [m["name"] for m in result.structured_content["matches"]] == names


async def test_get_requests_are_cached(client: Client, upstream: Upstream):
    await client.call_tool("skills", {})
    await client.call_tool("skills", {})
    await client.call_tool("check_skill", {"skill_name": "python"})
    assert [r.url.path for r in upstream.requests].count("/api/skills") == 1


async def test_upstream_error_becomes_tool_error(client: Client):
    result = await client.call_tool("contact", {}, raise_on_error=False)
    assert result.is_error
    assert "HTTP 500" in result.content[0].text


async def test_send_contact_message(client: Client, upstream: Upstream):
    result = await client.call_tool("send_contact_message", {"message": "  Hello Dani  "})
    assert result.structured_content == {"ok": True, "received": {"message": "Hello Dani"}}
    assert upstream.requests[-1].method == "POST"


async def test_send_contact_message_rejects_empty(client: Client, upstream: Upstream):
    result = await client.call_tool("send_contact_message", {"message": ""}, raise_on_error=False)
    assert result.is_error
    assert not upstream.requests


async def test_prompts(client: Client):
    prompts = {p.name for p in await client.list_prompts()}
    assert prompts == {"about_me_prompt", "tech_prompt"}
    result = await client.get_prompt("tech_prompt", {"tech": "Rust"})
    assert "check_skill" in result.messages[0].content.text


async def test_http_app_health():
    from starlette.testclient import TestClient

    from server import app

    with TestClient(app) as http:
        assert http.get("/health").json()["status"] == "ok"
