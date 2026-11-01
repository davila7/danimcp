# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DaniMCP is a Python Model Context Protocol (MCP) server (`python_dani_mcp/`) that exposes Daniel Avila's professional information through tools, prompts and MCP Apps UI views. Data comes from the backend API at `https://www.danielavila.me/api` (override with `DANIMCP_API_BASE_URL`). It supports stdio and Streamable HTTP, and is deployed to Vercel as a remote MCP server.

The former TypeScript implementation was removed; only the Python server exists.

## Commands

```bash
cd python_dani_mcp
uv sync                                   # install (incl. dev group)
uv run python server.py                   # stdio
uv run python server.py --http            # Streamable HTTP on :8000/mcp
uv run uvicorn server:app --port 8000     # same ASGI app Vercel runs
uv run fastmcp run server.py:mcp          # via FastMCP CLI
uv run pytest                             # tests (mocked upstream, no network)
uv run ruff check . && uv run ruff format --check .
```

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/). Dependencies: `fastmcp>=4.1.4,<5`, `httpx2`. Keep `requirements.txt` (used by Vercel) in sync with `pyproject.toml`.

## Architecture

- `server.py` — `create_server(api=None)` factory; registers tools, prompts, views and a `/health` route. Module-level exports: `mcp` (and alias `server`) for stdio, `app` = `mcp.http_app(path="/mcp", stateless_http=True)` for HTTP/Vercel.
- `api.py` — `DaniAPI`: async `httpx2` client, a new client per request (serverless-safe), 5-min per-process TTL cache for GETs, upstream failures raised as `ToolError` with a readable message. Accepts a `transport` for tests.
- `tools.py` — `register_tools(mcp, api)`: 9 async tools. All return `ToolResult(structured_content=...)`; list responses are wrapped in an object (`{"technologies": [...]}`, `{"projects": [...]}`) because `structuredContent` must be an object. `check_skill` is computed locally from `/skills` + `/technologies`.
- `prompts.py` — `about_me_prompt`, `tech_prompt(tech?)`; they tell the model which tools to use.
- `views.py` + `views/` — MCP Apps UI resources.
- `tests/test_server.py` — in-memory `fastmcp.Client` against `httpx2.MockTransport`.

### Known upstream issues (backend, not this repo)

- `GET /api/contact` and `GET /api/skills/{name}` return HTTP 500. `contact` surfaces it as a tool error; `check_skill` no longer depends on `/skills/{name}`.
- `/api/technologies` mixes `level` and `Level` keys — normalized to lower-case in `tools.py`.

### MCP Apps UI Views

Follows the [MCP Apps spec (2026-01-26)](https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx). Tools link to views with `app=AppConfig(resource_uri=...)` (serialized to `_meta.ui.resourceUri`):

| Tool | Resource | File |
|------|----------|------|
| `about_me` | `ui://danimcp/profile` | `profile.html` |
| `skills` | `ui://danimcp/skills-chart` | `skills_chart.html` (bars: skills per category + expandable lists) |
| `technologies` | `ui://danimcp/tech-chart` | `tech_chart.html` (counts + chips grouped by level) |
| `projects` | `ui://danimcp/projects` | `projects.html` |

Views use the `App` class from `@modelcontextprotocol/ext-apps@2.0.4` (`app-with-deps.js` from jsDelivr), read `result.structuredContent`, apply host theme/style variables, route link clicks through `app.openLink`, and escape all API data before inserting HTML. No Chart.js.

Shared code lives in `views/_shared.css` and `views/_shared.js` and is inlined into each view at the `/*@shared.css*/` and `/*@shared.js*/` markers when the resource is read (hosts render a single HTML document per resource). Every view must contain both markers.

#### Critical implementation rules (hard-won fixes)

1. **URI scheme must be `ui://`** — not `app://`. Hosts only recognize `ui://`.
2. **`mimeType` must be exactly `"text/html;profile=mcp-app"`** — hosts do a strict equality check. In FastMCP 4 this is the default for `ui://` resources returning `str`; the tests assert it.
3. **CSP must be declared on the resource** via `app=AppConfig(csp=ResourceCSP(...))`. The sandboxed iframe blocks all external origins otherwise. Any new CDN must be added to `views.CSP` (a test fails if a view references a `.js` URL outside jsDelivr).
4. **API requests need an explicit `User-Agent`** — Cloudflare in front of `danielavila.me` returns 403 without it. Set in `api.DEFAULT_HEADERS`.
5. **Keep `output_schema=None` on tools** — auto-generated output schemas (e.g. `nonNegativeInteger`) broke Claude Desktop's ajv validator. `structuredContent` is still sent without an `outputSchema`.
6. **Register `ontoolresult` before `await app.connect()`** — the tool result is a one-shot notification.
7. **Don't use `min-height: 100vh` in views** — the App auto-resizes the iframe to the content and a viewport-relative height causes resize loops.
8. **`stateless_http` goes to `http_app()` / `run()`**, not to the `FastMCP()` constructor (removed in FastMCP 4).

## Vercel Deployment

Files: `python_dani_mcp/vercel.json` (routes everything to `server.py` via `@vercel/python`), `requirements.txt`, `.vercelignore`.

**CRITICAL: Before any Vercel deploy, always run `vercel link --project <project-name> --yes` from the deploy directory. Vercel may default to another project in the account otherwise.**

```bash
cd python_dani_mcp && vercel link --project danimcp --yes && vercel deploy
```

**Local iteration loop (test before deploying):**
```bash
# Terminal 1
cd python_dani_mcp && uv run python server.py --http
# Terminal 2
npx @modelcontextprotocol/inspector
# → Transport: Streamable HTTP → URL: http://localhost:8000/mcp → Connect → Apps tab → run a tool
```

Only push to git (triggering a Vercel deploy) once the UI renders correctly in the Inspector locally.

## Claude Desktop Configuration

### Local (stdio)
```json
{
  "mcpServers": {
    "DaniMCP": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/python_dani_mcp", "python", "server.py"]
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
