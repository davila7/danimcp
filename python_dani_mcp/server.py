"""DaniMCP — MCP server exposing Daniel Avila's professional information.

Entry points:
- ``mcp`` / ``server``: FastMCP instance (``fastmcp run server.py:mcp``)
- ``app``: ASGI app for Streamable HTTP at ``/mcp`` (uvicorn / Vercel)
- ``python server.py [--http]``: stdio by default, HTTP with ``--http``
"""

from __future__ import annotations

import os
import sys

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from api import DaniAPI
from prompts import register_prompts
from tools import register_tools
from views import register_views

SERVER_NAME = "DaniMCP"
SERVER_VERSION = "2.0.0"

INSTRUCTIONS = """\
Tools for answering questions about Daniel Avila (AI Software Engineer, creator of Claude Code Templates).
Use `about_me`, `skills`, `technologies`, `projects` and `talks` for facts.
Prefer `check_skill` for yes/no questions about a specific skill.
`send_contact_message` delivers a real message to Daniel: only use it when the user explicitly asks,
after confirming the text with them.
"""


def create_server(api: DaniAPI | None = None) -> FastMCP:
    mcp = FastMCP(
        SERVER_NAME,
        instructions=INSTRUCTIONS,
        version=SERVER_VERSION,
        website_url="https://www.danielavila.me",
        # Tool errors are raised as ToolError with safe messages; hide anything else.
        mask_error_details=True,
    )
    api = api or DaniAPI()
    register_tools(mcp, api)
    register_prompts(mcp)
    register_views(mcp)

    @mcp.custom_route("/health", methods=["GET"])
    async def health(_: Request) -> JSONResponse:
        return JSONResponse({"status": "ok", "name": SERVER_NAME, "version": SERVER_VERSION})

    return mcp


mcp = create_server()
server = mcp  # backwards-compatible name for `fastmcp run server.py:server`

# Stateless Streamable HTTP: no session affinity needed, so it works on serverless (Vercel).
app = mcp.http_app(path="/mcp", stateless_http=True)


if __name__ == "__main__":
    if "--http" in sys.argv:
        mcp.run(
            transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), path="/mcp", stateless_http=True
        )
    else:
        mcp.run()
