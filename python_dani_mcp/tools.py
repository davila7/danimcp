# File: tools.py
import json
from typing import Dict, Any, List
from mcp.types import TextContent
import urllib

class DaniMCPTools:
    """Tools implementation for Daniel Avila's MCP server"""
    
    def __init__(self):
        self._base_url = "https://danielavila.me/api"
        
    def _fetch_api_data(self, endpoint: str) -> Dict[str, Any]:
        """Helper method to fetch data from the API"""
        try:
            response = urllib.request.urlopen(f"{self._base_url}/{endpoint}")
            if response.getcode() == 200:
                return json.loads(response.read())
            else:
                raise Exception(f"Error: Response code {response.getcode()}")
        except Exception as e:
            raise Exception(f"Error fetching data from API: {str(e)}")
    
    def _format_response(self, data: Dict[str, Any]) -> Dict[str, List[TextContent]]:
        """Formats data for MCP response"""
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
        """Gets information about technologies Daniel Avila uses"""
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