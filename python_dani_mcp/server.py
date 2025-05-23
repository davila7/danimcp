# File: server.py
from mcp.server.fastmcp import FastMCP

import tools
import prompts

class DaniMCPServer:
    """Main class for Daniel Avila's MCP server"""

    def __init__(self, name: str = "DaniMCP Python Server"):
        self.name = name
        self.mcp = FastMCP(name)
        self.tools = tools.DaniMCPTools()
        self.prompts = prompts.DaniMCPPrompts()
        self._register_tools()
        self._register_prompts()

    def _register_tools(self) -> None:
        """Registers all available tools in the MCP server"""
        self.mcp.tool()(self.tools.hello)
        self.mcp.tool()(self.tools.about_me)
        self.mcp.tool()(self.tools.technologies)
        self.mcp.tool()(self.tools.projects)
        self.mcp.tool()(self.tools.contact)
        self.mcp.tool()(self.tools.send_contact_message)
        self.mcp.tool()(self.tools.talks)
        self.mcp.tool()(self.tools.skills)
        self.mcp.tool()(self.tools.check_skill)

    def _register_prompts(self) -> None:
        """Registers all available prompts in the MCP server"""
        self.mcp.prompt()(self.prompts.about_me_prompt)
        self.mcp.prompt()(self.prompts.tech_prompt)

    def run(self, transport: str = "stdio") -> None:
        """Runs the MCP server with the specified transport"""
        self.mcp.run(transport=transport)

# Create a server instance at the module level
server = DaniMCPServer().mcp

# Main entry point
if __name__ == "__main__":
    server.run()
