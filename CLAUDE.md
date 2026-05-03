# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DaniMCP is a Model Context Protocol (MCP) server with two parallel implementations (Python and TypeScript) that expose Daniel Avila's professional information through tools and prompts. Both versions communicate with the backend API at `https://www.danielavila.me/api`. The Python server supports both stdio and Streamable HTTP transports, and can be deployed to Vercel as a remote MCP server.

## Commands

### Python (`python_dani_mcp/`)

```bash
# Install dependencies
cd python_dani_mcp && uv sync

# Run the server
uv run fastmcp run server.py:server

# Run with stdio
uv run python server.py

# Run with Streamable HTTP (local)
cd python_dani_mcp && uv run uvicorn server:app --host 0.0.0.0 --port 8000
```

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

### TypeScript (`typescript_dani_mcp/`)

```bash
# Install dependencies
cd typescript_dani_mcp && npm install

# Compile
npx tsc

# Run
node dist/server.js
```

No test or lint commands are configured in either project.

## Architecture

Both implementations share an identical three-layer structure:

- **Server** (`server.py` / `server.ts`) — Initializes the MCP server, registers tools and prompts. This is the entry point.
- **Tools** (`tools.py` / `tools.ts`) — 8 tools (`hello`, `about_me`, `technologies`, `projects`, `contact`, `send_contact_message`, `talks`, `skills`) that make HTTP requests to the API. All tools use GET except `send_contact_message` (POST).
- **Prompts** (`prompts.py` / `prompts.ts`) — 2 prompt templates: `about_me_prompt` and `tech_prompt` (accepts optional technology filter).

Python uses `fastmcp>=3.0.0b1` (FastMCP 3.0 standalone) and `urllib.request` for HTTP. TypeScript uses `@modelcontextprotocol/sdk` with `McpServer` and native `fetch`.

The Python server exports two module-level objects:
- `server` — FastMCP instance for stdio transport (`uv run python server.py`)
- `app` — ASGI app (Starlette) for Streamable HTTP transport, created with `stateless_http=True` for serverless compatibility. The MCP endpoint is mounted at `/mcp`.

### MCP Apps UI Views (Python only)

The Python server registers 4 HTML resources following the [MCP Apps spec (2026-01-26)](https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx). Tools link to UI views via `_meta.ui.resourceUri`:

- `ui://danimcp/skills-chart` — Radar chart of skills by category (Chart.js)
- `ui://danimcp/tech-chart` — Horizontal bar chart of technologies by proficiency
- `ui://danimcp/profile` — Profile card with personal info
- `ui://danimcp/projects` — Card grid of featured projects

Views are self-contained HTML files in `python_dani_mcp/views/` that use Chart.js CDN and the `@modelcontextprotocol/ext-apps` App class for host communication.

#### Critical implementation rules (hard-won fixes)

**1. URI scheme must be `ui://`** — not `app://`. Hosts (Claude.ai, Inspector) only recognize `ui://`.

**2. Resources must return `ResourceResult([ResourceContent(...)])`, not a plain string.**
FastMCP defaults string returns to `mimeType: "text/plain"`, which hosts reject. The correct pattern:
```python
from fastmcp.resources import ResourceContent, ResourceResult

@mcp.resource(uri, ...)
def my_view() -> ResourceResult:
    return ResourceResult([ResourceContent(Path("view.html").read_text(), mime_type="text/html;profile=mcp-app")])
```

**3. `mimeType` must be exactly `"text/html;profile=mcp-app"`** — MCP Inspector (and Claude.ai) do a strict equality check against this string. `"text/html"` alone is rejected.

**4. CSP must be declared on the resource via `meta=`** — the sandboxed iframe blocks all external origins by default. Declare allowed origins with `connectDomains` (fetch/XHR) and `resourceDomains` (scripts/CSS):
```python
UI_CSP = {
    "ui": {
        "csp": {
            "connectDomains": ["https://www.danielavila.me", "https://esm.sh"],
            "resourceDomains": ["https://esm.sh", "https://cdn.jsdelivr.net"],
        }
    }
}

@mcp.resource(uri, meta=UI_CSP, ...)
def my_view() -> ResourceResult: ...
```

**5. API requests need explicit `User-Agent` header** — the `danielavila.me` API is behind Cloudflare, which blocks Python's `urllib` default (no User-Agent) with 403. Always use:
```python
req = urllib.request.Request(url, headers={"User-Agent": "DaniMCP/1.0", "Accept": "application/json"})
```

## Vercel Deployment

The Python server can be deployed to Vercel as a remote MCP server with Streamable HTTP transport.

**Files involved:**
- `python_dani_mcp/vercel.json` — Vercel build and routing config (routes all requests to `server.py` via `@vercel/python`)
- `python_dani_mcp/requirements.txt` — Dependencies for Vercel's Python builder

**CRITICAL: Before any Vercel deploy, always run `vercel link --project <project-name> --yes` from the deploy directory to ensure the deploy targets the correct project. Vercel may default to another project in the account otherwise.**

**Deploy:**
```bash
cd python_dani_mcp && vercel link --project danimcp --yes && vercel deploy
```

**Local iteration loop (test before deploying):**
```bash
# Terminal 1 — start local server
cd python_dani_mcp && uv run uvicorn server:app --host 0.0.0.0 --port 8000

# Terminal 2 — start MCP Inspector
npx @modelcontextprotocol/inspector
# → Transport: Streamable HTTP → URL: http://localhost:8000/mcp → Connect
# → Apps tab → click a tool → UI should render in the right panel
```

Only push to git (triggering Vercel deploy) once the UI renders correctly in the Inspector locally.

## Claude Desktop Configuration

### Local (stdio)
```json
{
  "mcpServers": {
    "DaniMCP Python Server": {
      "command": "/path/to/uv",
      "args": ["run", "--with", "fastmcp", "fastmcp", "run", "/path/to/python_dani_mcp/server.py:server"]
    }
  }
}
```

### Remote (Streamable HTTP via Vercel)
```json
{
  "mcpServers": {
    "DaniMCP": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://<app>.vercel.app/mcp"]
    }
  }
}
```
