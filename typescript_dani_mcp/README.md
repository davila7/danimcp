# TypeScript Dani MCP Server

This project contains a TypeScript server as part of the Dani MCP system.

## Features
- **hello**: This command returns a greeting message.
- **about_me**: This command returns information about the server.
- **technologies**: This command returns a list of Dani's technologies.
- **projects**: This command returns a list of Dani's projects.
- **contact**: This command returns a list of Dani's contact information.

## How to use
Clone the repository and run the server using the command provided below.

```bash
npx -y tsx /path/to/projects/danimcp/typescript_dani_mcp/main.ts
```

## Usage with CodeGPT
### NPX

Add this to your `.codegpt/mcp_config.json` file:
```json
{
  "mcpServers": {
    "DaniMCPTypescriptServer": {
      "command": "npx",
      "args": [
        "-y",
        "tsx",
        "/path/to/projects/danimcp/typescript_dani_mcp/dist/main.ts"
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
    "DaniMCPTypescriptServer": {
      "command": "npx",
      "args": [
        "-y",
        "tsx",
        "/path/to/projects/danimcp/typescript_dani_mcp/dist/main.ts"
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
      "filesystem": {
        "command": "npx",
        "args": [
          "-y",
          "tsx",
          "/path/to/projects/danimcp/typescript_dani_mcp/dist/main.ts"
        ]
      }
    }
  }
}
```

## Example questions to use the tools
- Use the tool about_me and explain who is Daniel 
- Use the tool projects to know about the projects of Daniel
- Use the tool technologies and tell me if Daniel knows about python and MCP

The model will use the tools to answer the questions, but first it will ask for confirmation to use the tools.

[add image]

Then the model will read the API response and answer the question.

[add image]