"""Prompt templates that steer the model towards the right tools."""

from __future__ import annotations

from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field


def register_prompts(mcp: FastMCP) -> None:
    @mcp.prompt(title="About Daniel")
    def about_me_prompt() -> str:
        """Get an overview of Daniel Avila's background and work."""
        return (
            "Give me a concise overview of Daniel Avila. Use the `about_me` tool for the profile, "
            "`skills` for areas of expertise and `projects` for featured work. "
            "Summarize who Daniel is, current focus, and two or three highlights."
        )

    @mcp.prompt(title="Technical expertise")
    def tech_prompt(
        tech: Annotated[str | None, Field(description="Optional technology to focus on, e.g. Python")] = None,
    ) -> str:
        """Explore Daniel Avila's technical expertise, optionally focused on one technology."""
        if tech:
            return (
                f"Does Daniel Avila have experience with {tech}? Use the `check_skill` tool with "
                f'skill_name="{tech}", then `technologies` for the proficiency level. '
                "Answer directly and cite where the skill appears."
            )
        return (
            "Describe Daniel Avila's technical background. Use the `technologies` and `skills` tools "
            "and group the answer by area, highlighting advanced-level technologies."
        )
