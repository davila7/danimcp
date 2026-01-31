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

### ext-apps UI Views (Python only)

The Python server registers 4 HTML resources following the [MCP ext-apps](https://modelcontextprotocol.github.io/ext-apps/) spec. Tools link to UI views via `_meta.ui.resourceUri`:

- `app://danimcp/skills-chart` — Radar chart of skills by category (Chart.js)
- `app://danimcp/tech-chart` — Horizontal bar chart of technologies by proficiency
- `app://danimcp/profile` — Profile card with personal info
- `app://danimcp/projects` — Card grid of featured projects

Views are self-contained HTML files in `python_dani_mcp/views/` that use Chart.js CDN and the `@modelcontextprotocol/ext-apps` App class for host communication.

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

**Verify with MCP Inspector:**
```bash
npx @modelcontextprotocol/inspector
# → Select Streamable HTTP → http://localhost:8000/mcp (local) or https://<app>.vercel.app/mcp (remote)
```

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
