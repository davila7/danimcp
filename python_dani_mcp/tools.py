"""Tools that expose Daniel Avila's professional information."""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp.apps import AppConfig
from fastmcp.tools import ToolResult
from pydantic import Field

from api import DaniAPI
from views import VIEWS

# All read tools hit an external API whose data does not change between calls.
READ_ONLY = {"readOnlyHint": True, "idempotentHint": True, "openWorldHint": True}


def _ui(view: str) -> AppConfig:
    return AppConfig(resource_uri=VIEWS[view].uri)


def _iter_leaves(node: Any, path: tuple[str, ...] = ()) -> Iterator[tuple[tuple[str, ...], str]]:
    """Yield (category path, value) for every string leaf in a nested skills tree."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _iter_leaves(value, (*path, key))
    elif isinstance(node, list):
        for value in node:
            yield from _iter_leaves(value, path)
    elif isinstance(node, str):
        yield path, node


def _matches(query: str, value: str) -> bool:
    """Case-insensitive whole-token match, so "Java" does not match "JavaScript"."""
    pattern = rf"(?<![a-z0-9]){re.escape(query.lower())}(?![a-z0-9])"
    return re.search(pattern, value.lower()) is not None


def _normalize_technologies(raw: Any) -> list[dict[str, Any]]:
    """Lower-case keys: upstream data mixes `level` and `Level`."""
    if not isinstance(raw, list):
        return []
    return [{str(k).lower(): v for k, v in item.items()} for item in raw if isinstance(item, dict)]


def register_tools(mcp: FastMCP, api: DaniAPI) -> None:
    # output_schema=None on every tool: auto-generated output schemas have broken
    # Claude Desktop's ajv validator before (e.g. `nonNegativeInteger`).
    # structuredContent is still sent; it's what the UI views consume.

    @mcp.tool(title="Hello", annotations=READ_ONLY, output_schema=None)
    async def hello() -> ToolResult:
        """Get a short greeting from Daniel Avila."""
        return ToolResult(structured_content=await api.get("hello"))

    @mcp.tool(title="About Daniel", annotations=READ_ONLY, output_schema=None, app=_ui("profile"))
    async def about_me() -> ToolResult:
        """Get Daniel Avila's profile: name, occupation, location, age and education."""
        return ToolResult(structured_content=await api.get("about_me"))

    @mcp.tool(title="Technologies", annotations=READ_ONLY, output_schema=None, app=_ui("tech_chart"))
    async def technologies() -> ToolResult:
        """List the technologies Daniel Avila works with and the proficiency level for each."""
        return ToolResult(structured_content={"technologies": _normalize_technologies(await api.get("technologies"))})

    @mcp.tool(title="Projects", annotations=READ_ONLY, output_schema=None, app=_ui("projects"))
    async def projects() -> ToolResult:
        """List Daniel Avila's featured projects with descriptions and links."""
        return ToolResult(structured_content={"projects": await api.get("projects")})

    @mcp.tool(title="Contact info", annotations=READ_ONLY, output_schema=None)
    async def contact() -> ToolResult:
        """Get Daniel Avila's contact information and social links."""
        return ToolResult(structured_content=await api.get("contact"))

    @mcp.tool(
        title="Send contact message",
        annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
        output_schema=None,
    )
    async def send_contact_message(
        message: Annotated[
            str,
            Field(
                min_length=1,
                max_length=2000,
                description="The message to send to Daniel. Include how to reach you back if you expect a reply.",
            ),
        ],
    ) -> ToolResult:
        """Send a message to Daniel Avila through the danielavila.me contact form.

        Only call this when the user explicitly asks to send a message, and confirm the content first.
        """
        result = await api.post("contact", {"message": message.strip()})
        return ToolResult(structured_content=result if isinstance(result, dict) else {"result": result})

    @mcp.tool(title="Talks", annotations=READ_ONLY, output_schema=None)
    async def talks() -> ToolResult:
        """Get Daniel Avila's talks, workshops and community involvement, grouped by country."""
        return ToolResult(structured_content=await api.get("talks"))

    @mcp.tool(title="Skills", annotations=READ_ONLY, output_schema=None, app=_ui("skills_chart"))
    async def skills() -> ToolResult:
        """Get Daniel Avila's skills grouped by category (programming, AI/LLM tools, cloud, etc.)."""
        return ToolResult(structured_content=await api.get("skills"))

    @mcp.tool(title="Check skill", annotations=READ_ONLY, output_schema=None)
    async def check_skill(
        skill_name: Annotated[
            str,
            Field(
                min_length=1,
                max_length=100,
                description='Skill or technology to look up, e.g. "Python" or "LangChain".',
            ),
        ],
    ) -> ToolResult:
        """Check whether Daniel Avila has a specific skill or technology, and where it appears in the profile."""
        query = skill_name.strip()
        skills_data = await api.get("skills")
        technologies_data = _normalize_technologies(await api.get("technologies"))

        matches: list[dict[str, Any]] = [
            {"source": "skills", "category": " > ".join(path), "name": value}
            for path, value in _iter_leaves(skills_data)
            if _matches(query, value)
        ]
        matches += [
            {"source": "technologies", "name": t["name"], "level": t.get("level")}
            for t in technologies_data
            if isinstance(t.get("name"), str) and _matches(query, t["name"])
        ]
        return ToolResult(structured_content={"skill": query, "has_skill": bool(matches), "matches": matches})
