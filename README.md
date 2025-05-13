# DaniMCP Servers
This repository contains the source code for run python and typescript servers for DaniMCP.

# API Endpoints
This MCP Server allows you to interact with this API endpoints:
- **Base URL**: `https://danielavila.me`
- **/api/hello**: Simple endpoint to test the server.
- **/api/about_me**: Endpoint to get information about me.
- **/api/technologies**: Endpoint to get a list of technologies I know.
- **/api/projects**: Endpoint to get a list of my projects.
- **/api/contact**: Endpoint to get my contact information.

# Servers list
- [DaniMCP Python Server](https://github.com/davila7/danimcp/tree/main/python_dani_mcp)
- [DaniMCP Typescript Server](https://github.com/davila7/danimcp/tree/main/typescript_dani_mcp)

# Tool list 
- **hello**: This command returns a greeting message.
- **about_me**: This command returns information about the server.
- **technologies**: This command returns a list of Dani's technologies.
- **projects**: This command returns a list of Dani's projects.
- **contact**: This command returns a list of Dani's contact information.

## Example questions to use the tools
- Use the tool about_me and explain who is Daniel 
- Use the tool projects to know about the projects of Daniel
- Use the tool technologies and tell me if Daniel knows about python and MCP

The model will use the tools to answer the questions, but first it will ask for confirmation to use the tools.

![Screenshot 2025-05-09 at 15 39 52](https://github.com/user-attachments/assets/72aea146-7889-4172-9b15-2cfed780022a)

Then the model will read the API response and answer the question.

![Screenshot 2025-05-09 at 15 40 09](https://github.com/user-attachments/assets/e8f4f3fe-cfec-420b-8999-dd9b08b204ec)


# Python Server
The Python server is a simple server that returns a greeting message.

## Intall UV
To install UV, run the following command:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation
Go to the python_dani_mcp folder and run the following command:
```bash
cd python_dani_mcp
```

Then add MCP to your project dependencies:
```bash
uv add "mcp[cli]"
```

To install the Python server, run the following command:
```bash
uv run mcp install main.py
```

## Add the server to the MCP
To add the server to the MCP, run the following command:
```bash
uv run mcp add main.py
```