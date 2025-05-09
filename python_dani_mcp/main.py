# server.py
import urllib.request
import json
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# Create an MCP server
mcp = FastMCP("DaniMCP Python Server")

# Add an addition tool
@mcp.tool()
def about_me() -> str:

    # call the api danielavila.me/api/about_me
    # json example {"name":"Daniel Ávila Arias","age":37,"location":"Grand Rapids, MI, USA","occupation":"AI Software Engineer","education":"Bachelor of Science in Computer Science"}
    response_text = ""
    # utiliza
    response = urllib.request.urlopen("https://danielavila.me/api/about_me")
    if response.getcode() == 200:
        response_text = json.dumps(json.loads(response.read()), indent=4)
    else:
        response_text = "Error: Unable to fetch data"
    return {
        "content": [{
            "type": "text",
            "text": response_text
        }]
    }


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# prompts section
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"

@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]