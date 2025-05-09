# server.py
from mcp.server.fastmcp import FastMCP
import datetime
from mcp.server.fastmcp.prompts import base

# Create an MCP server
mcp = FastMCP("DaniMCP Python Server")


# function to calculate my age from my birthdate
def calculate_age(birthdate: datetime.date) -> str:
    today = datetime.date.today()
    age = today.year - birthdate.year
    m = today.month - birthdate.month
    if m < 0 or (m == 0 and today.day < birthdate.day):
        age -= 1
    return f"My age is : {age}"

about_me_input_schema = {
    "name": {"type": "string", "description": "Daniel Ávila Arias"},
    "age": {"type": "number", "description": calculate_age(datetime.date(1988, 1, 25))},
    "location": {"type": "string", "description": "Grand Rapids, Michigan, USA"},
    "occupation": {"type": "string", "description": "AI Software Engineer"},
    "education": {"type": "string", "description": "Computer Science"},
}

# Add an addition tool
@mcp.tool()
def about_me() -> str:
     # Accessing values from the schema description dictionary
    name = about_me_input_schema["name"]["description"]
    age = about_me_input_schema["age"]["description"]
    location = about_me_input_schema["location"]["description"]
    occupation = about_me_input_schema["occupation"]["description"]
    education = about_me_input_schema["education"]["description"]

    # Constructing the response string using f-string
    response_text = f"My name is {name}, {age} years old, I live in {location}, I am a {occupation} and I have a degree in {education}."

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