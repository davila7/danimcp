"""MCP Apps UI views (spec 2026-01-26), served as ``ui://`` HTML resources.

Each view in ``views/`` is an HTML document. Shared code is inlined when the
resource is read, because hosts render one HTML document per resource and cannot
load sibling files:

- ``views/_shared.css`` replaces the ``/*@shared.css*/`` marker (theme tokens)
- ``views/_shared.js`` replaces the ``/*@shared.js*/`` marker (host connection,
  theming, HTML escaping)
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from pathlib import Path

from fastmcp import FastMCP
from fastmcp.apps import AppConfig, ResourceCSP

VIEWS_DIR = Path(__file__).parent / "views"
SHARED_FILES = {"/*@shared.css*/": "_shared.css", "/*@shared.js*/": "_shared.js"}

# The sandboxed iframe blocks every external origin unless declared here.
# Views only load the ext-apps SDK from jsDelivr; all data comes from tool results.
CSP = ResourceCSP(
    resource_domains=["https://cdn.jsdelivr.net"],
    connect_domains=["https://cdn.jsdelivr.net"],
)


@dataclass(frozen=True)
class View:
    uri: str
    file: str
    title: str
    description: str


VIEWS: dict[str, View] = {
    "profile": View("ui://danimcp/profile", "profile.html", "Profile Card", "Daniel Avila's profile card"),
    "skills_chart": View(
        "ui://danimcp/skills-chart",
        "skills_chart.html",
        "Skills Chart",
        "Number of skills per category, with the full list",
    ),
    "tech_chart": View(
        "ui://danimcp/tech-chart", "tech_chart.html", "Technologies Chart", "Technologies by proficiency level"
    ),
    "projects": View("ui://danimcp/projects", "projects.html", "Projects Gallery", "Card grid of featured projects"),
}


@cache
def render_view(file: str) -> str:
    html = (VIEWS_DIR / file).read_text(encoding="utf-8")
    for marker, shared_file in SHARED_FILES.items():
        if marker not in html:
            raise ValueError(f"{file} is missing the {marker} marker")
        html = html.replace(marker, (VIEWS_DIR / shared_file).read_text(encoding="utf-8"), 1)
    return html


def register_views(mcp: FastMCP) -> None:
    for key, view in VIEWS.items():

        def make_reader(file: str):
            def read() -> str:
                return render_view(file)

            return read

        # ui:// URIs default to mimeType "text/html;profile=mcp-app" in FastMCP 4.
        mcp.resource(
            view.uri,
            name=key,
            title=view.title,
            description=view.description,
            app=AppConfig(csp=CSP),
        )(make_reader(view.file))
