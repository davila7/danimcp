# DaniMCP

MCP server that exposes Daniel Avila's professional information (profile, skills, technologies, projects, talks, contact) through tools, prompts and [MCP Apps](https://github.com/modelcontextprotocol/ext-apps) UI views.

Built with [FastMCP 4](https://gofastmcp.com). Data comes from `https://www.danielavila.me/api`.

## Tools

| Tool | Description | UI view |
|------|-------------|---------|
| `hello` | Short greeting | — |
| `about_me` | Profile: name, occupation, location, education | Profile card |
| `skills` | Skills grouped by category | Skills per category |
| `check_skill` | Does Daniel have skill X, and where does it appear | — |
| `technologies` | Technologies and proficiency level | Technologies by level |
| `projects` | Featured projects | Projects gallery |
| `talks` | Talks and community involvement | — |
| `contact` | Contact information | — |
| `send_contact_message` | Sends a message through the website contact form | — |

All tools return `structuredContent` (plus the same JSON as text). Read tools are annotated `readOnlyHint`.

## Prompts

- `about_me_prompt` — overview of Daniel using `about_me`, `skills` and `projects`
- `tech_prompt(tech?)` — technical background, or a focused check on one technology

## Run locally

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
cd python_dani_mcp
uv sync

uv run python server.py            # stdio
uv run python server.py --http     # Streamable HTTP on http://localhost:8000/mcp
uv run pytest                      # tests (mocked upstream, no network)
uv run ruff check .                # lint
```

Test the UI views with the MCP Inspector: `npx @modelcontextprotocol/inspector` → Transport *Streamable HTTP* → `http://localhost:8000/mcp` → Apps tab.

## Client configuration

### Claude Desktop (stdio)

```json
{
  "mcpServers": {
    "DaniMCP": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/danimcp/python_dani_mcp", "python", "server.py"]
    }
  }
}
```

### Remote (Streamable HTTP)

Add `https://<your-deployment>/mcp` as a custom connector in Claude, or for clients that only speak stdio:

```json
{
  "mcpServers": {
    "DaniMCP": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://<your-deployment>/mcp"]
    }
  }
}
```

## Deploy to Vercel

```bash
cd python_dani_mcp
vercel link --project danimcp --yes
vercel deploy
```

The ASGI app (`server:app`) runs stateless Streamable HTTP at `/mcp`, with a health check at `/health`.
