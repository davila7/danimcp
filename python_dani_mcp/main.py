# File: server.py
import json
import urllib.request
from typing import Dict, Any, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.types import Image
from mcp.types import TextContent


class DaniMCPServer:
    """
    Main class for Daniel Avila's MCP server.
    Implements tools to retrieve information from danielavila.me API
    """
    
    def __init__(self, name: str = "DaniMCP Python Server"):
        """
        Initializes the MCP server with a custom name.
        
        Args:
            name: Name of the MCP server
        """
        self.mcp = FastMCP(name)
        self._register_tools()
        
    def _register_tools(self) -> None:
        """Registers all available tools in the MCP server"""
        self.mcp.tool()(self.hello)
        self.mcp.tool()(self.about_me)
        self.mcp.tool()(self.technologies)
        self.mcp.tool()(self.projects)
        self.mcp.tool()(self.contact)
        
    def _fetch_api_data(self, endpoint: str) -> Dict[str, Any]:
        """
        Helper method to fetch data from the API.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Data retrieved from the API as a dictionary
            
        Raises:
            Exception: If there's an error retrieving the data
        """
        try:
            response = urllib.request.urlopen(f"https://danielavila.me/api/{endpoint}")
            if response.getcode() == 200:
                return json.loads(response.read())
            else:
                raise Exception(f"Error: Response code {response.getcode()}")
        except Exception as e:
            raise Exception(f"Error fetching data from API: {str(e)}")
    
    def _format_response(self, data: Dict[str, Any]) -> Dict[str, List[TextContent]]:
        """
        Formats data for MCP response.
        
        Args:
            data: Data to format
            
        Returns:
            Formatted response for MCP
        """
        return {
            "content": [
                TextContent(
                    type="text",
                    text=json.dumps(data, indent=4)
                )
            ]
        }
    
    def hello(self) -> Dict[str, List[TextContent]]:
        """Gets a greeting from the API"""
        data = self._fetch_api_data("hello")
        return self._format_response(data)
    
    def about_me(self) -> Dict[str, List[TextContent]]:
        """Gets information about Daniel Avila"""
        data = self._fetch_api_data("about_me")
        return self._format_response(data)
    
    def technologies(self) -> Dict[str, List[TextContent]]:
        """Gets information about technologies Daniel Avila uses and knows"""
        data = self._fetch_api_data("technologies")
        return self._format_response(data)
    
    def projects(self) -> Dict[str, List[TextContent]]:
        """Gets information about Daniel Avila's projects"""
        data = self._fetch_api_data("projects")
        return self._format_response(data)
    
    def contact(self) -> Dict[str, List[TextContent]]:
        """Gets Daniel Avila's contact information"""
        data = self._fetch_api_data("contact")
        return self._format_response(data)
    
    def run(self, transport: str = "stdio") -> None:
        """
        Runs the MCP server with the specified transport.
        
        Args:
            transport: Transport type ("stdio", "sse", or "streamable-http")
        """
        self.mcp.run(transport=transport)


# Main entry point
if __name__ == "__main__":
    server = DaniMCPServer()
    server.run()