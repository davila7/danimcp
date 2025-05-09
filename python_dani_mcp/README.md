# Python Dani MCP Server
This project contains a Python server as part of the Dani MCP system.

## Features
- **hello**: This command returns a greeting message.
- **about_me**: This command returns information about the server.
- **technologies**: This command returns a list of Dani's technologies.
- **projects**: This command returns a list of Dani's projects.
- **contact**: This command returns a list of Dani's contact information.
- 
## How to use
Clone the repository and run the server using the command provided below.

go to python_dani_mcp and run the following command:
```bash
/Users/users/.local/bin/uv run mcp install main.py
```

## Usage with CodeGPT

### UV
Add this to your `.codegpt/mcp_config.json` file:
```json
{
  "mcpServers": {
    "DaniMCP Python Server": {
      "command": "/Users/danipower/.local/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/path/to/projects/danimcp/python_dani_mcp/main.py"
      ]
    }
  }
}
```

## Usage with Claude Desktop
Add this to your `claude_desktop_config.json` file:
```json
{
  "mcpServers": {
    "DaniMCP Python Server": {
      "command": "/Users/danipower/.local/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/path/to/projects/danimcp/python_dani_mcp/main.py"
      ]
    }
  }
}
```

## Usage with VSCode
Add this to your `.vscode/mcp.json` file:
```json
{
  "mcp": {
    "servers": {
      "DaniMCP Python Server": {
        "command": "/Users/danipower/.local/bin/uv",
            "args": [
                    "run",
                    "--with",
                    "mcp[cli]",
                    "mcp",
                    "run",
                    "/path/to/projects/danimcp/python_dani_mcp/main.py"
                ]
            }
        }
    }
}
```

## Example questions to use the tools
- Use the tool about_me and explain who is Daniel 
- Use the tool projects to know about the projects of Daniel
- Use the tool technologies and teel me if Daniel knows about python and MCP