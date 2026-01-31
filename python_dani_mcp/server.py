# File: server.py
from pathlib import Path
from fastmcp import FastMCP

import tools
import prompts

VIEWS_DIR = Path(__file__).parent / "views"

# Resource URIs for ext-apps UI views
RESOURCE_URIS = {
    "skills": "app://danimcp/skills-chart",
    "technologies": "app://danimcp/tech-chart",
    "about_me": "app://danimcp/profile",
    "projects": "app://danimcp/projects",
}

class DaniMCPServer:
    """Main class for Daniel Avila's MCP server"""

    def __init__(self, name: str = "DaniMCP Python Server", stateless_http: bool = False):
        self.name = name
        self.mcp = FastMCP(name, stateless_http=stateless_http)
        self.tools = tools.DaniMCPTools()
        self.prompts = prompts.DaniMCPPrompts()
        self._register_tools()
        self._register_prompts()
        self._register_resources()

    def _register_tools(self) -> None:
        """Registers all available tools in the MCP server"""
        self.mcp.tool(output_schema=False)(self.tools.hello)
        self.mcp.tool(output_schema=False, meta={"ui": {"resourceUri": RESOURCE_URIS["about_me"]}})(self.tools.about_me)
        self.mcp.tool(output_schema=False, meta={"ui": {"resourceUri": RESOURCE_URIS["technologies"]}})(self.tools.technologies)
        self.mcp.tool(output_schema=False, meta={"ui": {"resourceUri": RESOURCE_URIS["projects"]}})(self.tools.projects)
        self.mcp.tool(output_schema=False)(self.tools.contact)
        self.mcp.tool(output_schema=False)(self.tools.send_contact_message)
        self.mcp.tool(output_schema=False)(self.tools.talks)
        self.mcp.tool(output_schema=False, meta={"ui": {"resourceUri": RESOURCE_URIS["skills"]}})(self.tools.skills)
        self.mcp.tool(output_schema=False)(self.tools.check_skill)

    def _register_prompts(self) -> None:
        """Registers all available prompts in the MCP server"""
        self.mcp.prompt()(self.prompts.about_me_prompt)
        self.mcp.prompt()(self.prompts.tech_prompt)

    def _register_resources(self) -> None:
        """Registers HTML UI resources for ext-apps visualization"""
        mime = "text/html; charset=utf-8"

        @self.mcp.resource(RESOURCE_URIS["skills"], mime_type=mime, title="Skills Chart", description="Radar chart of Daniel's skills by category")
        def skills_chart() -> str:
            return (VIEWS_DIR / "skills_chart.html").read_text()

        @self.mcp.resource(RESOURCE_URIS["technologies"], mime_type=mime, title="Technologies Chart", description="Bar chart of Daniel's technologies by proficiency")
        def tech_chart() -> str:
            return (VIEWS_DIR / "tech_chart.html").read_text()

        @self.mcp.resource(RESOURCE_URIS["about_me"], mime_type=mime, title="Profile Card", description="Daniel Avila's profile card")
        def profile_card() -> str:
            return (VIEWS_DIR / "profile.html").read_text()

        @self.mcp.resource(RESOURCE_URIS["projects"], mime_type=mime, title="Projects Gallery", description="Daniel Avila's featured projects")
        def projects_gallery() -> str:
            return (VIEWS_DIR / "projects.html").read_text()

    def run(self, transport: str = "stdio") -> None:
        """Runs the MCP server with the specified transport"""
        self.mcp.run(transport=transport)

# Create a server instance at the module level
server = DaniMCPServer().mcp

# ASGI app for Vercel deployment (Streamable HTTP)
app = DaniMCPServer(stateless_http=True).mcp.http_app(path="/mcp")

# Main entry point
if __name__ == "__main__":
    server.run()
