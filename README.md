# DaniMCP Servers
This repository contains the source code for run python and typescript servers for DaniMCP.

# Servers list
- [DaniMCP Python Server](https://github.com/davila7/danimcp/tree/main/python_dani_mcp)
- [DaniMCP Typescript Server](https://github.com/davila7/danimcp/tree/main/typescript_dani_mcp)

# Tool list 
- **hello**: This command returns a greeting message.
- **about_me**: This command returns information about the server.
- **skills**: This command returns a list of Dani's skills.
- **check_skill**: This command checks if Dani has a specific skill.
- **technologies**: This command returns a list of Dani's technologies.
- **projects**: This command returns a list of Dani's projects.
- **talks**: This command returns a list of Dani's talks.
- **contact**: This command returns a list of Dani's contact information.
- **send_contact_message**: This command sends a message to Dani.

# Prompts list
- **about_me_prompt**: This prompt is used to get information about Dani.
- **tech_prompt**: This prompt is used to get information about Dani's technologies.        

## Example questions to use the tools
- Use the tool about_me and explain who is Daniel 
- Use the tool projects to know about the projects that Daniel has done
- Send a message to Daniel using the tool send_contact_message
- Use the tool check_skill and tell me if Daniel knows about python
- Use the tool technologies and tell me if Daniel knows about python and MCP

# How this works
The model will use the tools to answer the questions, but first it will ask for confirmation to use the tools.

![Screenshot 2025-05-09 at 15 39 52](https://github.com/user-attachments/assets/72aea146-7889-4172-9b15-2cfed780022a)

Then the model will read the API response and answer the question.

![Screenshot 2025-05-09 at 15 40 09](https://github.com/user-attachments/assets/e8f4f3fe-cfec-420b-8999-dd9b08b204ec)


# Python Server instructions
The Python server is a simple server that returns a greeting message.

## Isntall UV
To install UV, run the following command:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation
Go to the python_dani_mcp folder and run the following command:
```bash
cd python_dani_mcp
```

To install the Python server, run the following command:
```bash
uv run mcp install server.py
```

or Add this to your `.codegpt/mcp_config.json` for CodeGPT or `/path/to/Claude/claude_desktop_config.json` for Claude Desktop:
```json
{
  "mcpServers": {
    "DaniMCP Python Server": {
      "command": "/path/to/uv/.local/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/path/to/projects/danimcp/python_dani_mcp/server.py"
      ]
    }
  }
}
```

# TypeScript Server instructions
(Comming soon)