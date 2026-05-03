# File: server.py
from pathlib import Path
from fastmcp import FastMCP
from fastmcp.resources import ResourceContent, ResourceResult

import tools
import prompts

VIEWS_DIR = Path(__file__).parent / "views"

# Resource URIs for ext-apps UI views
RESOURCE_URIS = {
    "skills": "ui://danimcp/skills-chart",
    "technologies": "ui://danimcp/tech-chart",
    "about_me": "ui://danimcp/profile",
    "projects": "ui://danimcp/projects",
}

UI_CSP = {
    "ui": {
        "csp": {
            "connectDomains": ["https://www.danielavila.me", "https://esm.sh"],
            "resourceDomains": ["https://esm.sh", "https://cdn.jsdelivr.net"],
        }
    }
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
        self.mcp.tool(output_schema=None)(self.tools.hello)
        self.mcp.tool(output_schema=None, meta={"ui": {"resourceUri": RESOURCE_URIS["about_me"]}})(self.tools.about_me)
        self.mcp.tool(output_schema=None, meta={"ui": {"resourceUri": RESOURCE_URIS["technologies"]}})(self.tools.technologies)
        self.mcp.tool(output_schema=None, meta={"ui": {"resourceUri": RESOURCE_URIS["projects"]}})(self.tools.projects)
        self.mcp.tool(output_schema=None)(self.tools.contact)
        self.mcp.tool(output_schema=None)(self.tools.send_contact_message)
        self.mcp.tool(output_schema=None)(self.tools.talks)
        self.mcp.tool(output_schema=None, meta={"ui": {"resourceUri": RESOURCE_URIS["skills"]}})(self.tools.skills)
        self.mcp.tool(output_schema=None)(self.tools.check_skill)

    def _register_prompts(self) -> None:
        """Registers all available prompts in the MCP server"""
        self.mcp.prompt()(self.prompts.about_me_prompt)
        self.mcp.prompt()(self.prompts.tech_prompt)

    def _register_resources(self) -> None:
        """Registers HTML UI resources for ext-apps visualization"""

        @self.mcp.resource(RESOURCE_URIS["skills"], title="Skills Chart", description="Radar chart of Daniel's skills by category", meta=UI_CSP)
        def skills_chart() -> ResourceContent:
            return ResourceResult([ResourceContent((VIEWS_DIR / "skills_chart.html").read_text(), mime_type="text/html;profile=mcp-app")])

        @self.mcp.resource(RESOURCE_URIS["technologies"], title="Technologies Chart", description="Bar chart of Daniel's technologies by proficiency", meta=UI_CSP)
        def tech_chart() -> ResourceContent:
            return ResourceResult([ResourceContent((VIEWS_DIR / "tech_chart.html").read_text(), mime_type="text/html;profile=mcp-app")])

        @self.mcp.resource(RESOURCE_URIS["about_me"], title="Profile Card", description="Daniel Avila's profile card", meta=UI_CSP)
        def profile_card() -> ResourceContent:
            return ResourceResult([ResourceContent((VIEWS_DIR / "profile.html").read_text(), mime_type="text/html;profile=mcp-app")])

        @self.mcp.resource(RESOURCE_URIS["projects"], title="Projects Gallery", description="Daniel Avila's featured projects", meta=UI_CSP)
        def projects_gallery() -> ResourceContent:
            return ResourceResult([ResourceContent((VIEWS_DIR / "projects.html").read_text(), mime_type="text/html;profile=mcp-app")])

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
