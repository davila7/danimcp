# server.py
import urllib.request
import json
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# Create an MCP server
mcp = FastMCP("DaniMCP Python Server")


@mcp.tool()
def hello() -> str:
    response_text = ""
    response = urllib.request.urlopen("https://danielavila.me/api/hello")
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

@mcp.tool()
def about_me() -> str:
    """Get information about me"""
    response_text = ""
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

@mcp.tool()
def technologies() -> str:
    """Get information about technologies I use and know"""
    response_text = ""
    response = urllib.request.urlopen("https://danielavila.me/api/technologies")
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

@mcp.tool()
def projects() -> str:
    """Get information about my projects"""
    response_text = ""
    response = urllib.request.urlopen("https://danielavila.me/api/projects")
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

@mcp.tool()
def contact() -> str:
    """Get information about how contact me"""
    response_text = ""
    response = urllib.request.urlopen("https://danielavila.me/api/contact")
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