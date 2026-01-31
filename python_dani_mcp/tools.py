# File: tools.py
import json
from typing import Dict, Any
import urllib.request

class DaniMCPTools:
    """Tools implementation for Daniel Avila's MCP server"""

    def __init__(self):
        self._base_url = "https://www.danielavila.me/api"

    def _fetch_api_data(self, endpoint: str) -> Dict[str, Any]:
        """Helper method to fetch data from the API (GET requests)"""
        try:
            response = urllib.request.urlopen(f"{self._base_url}/{endpoint}")
            if response.getcode() == 200:
                return json.loads(response.read())
            else:
                raise Exception(f"Error: Response code {response.getcode()}")
        except Exception as e:
            raise Exception(f"Error fetching data from API: {str(e)}")

    def _post_api_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Helper method to post data to the API (POST requests)"""
        try:
            data_encoded = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                f"{self._base_url}/{endpoint}",
                data=data_encoded,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    return json.loads(response.read())
                else:
                    raise Exception(f"Error: Response code {response.getcode()}")
        except Exception as e:
            raise Exception(f"Error posting data to API: {str(e)}")

    def hello(self) -> str:
        """Gets a greeting from the API"""
        data = self._fetch_api_data("hello")
        return json.dumps(data, indent=4)

    def about_me(self) -> str:
        """Gets information about Daniel Avila"""
        data = self._fetch_api_data("about_me")
        return json.dumps(data, indent=4)

    def technologies(self) -> str:
        """Gets information about technologies Daniel Avila uses"""
        data = self._fetch_api_data("technologies")
        return json.dumps(data, indent=4)

    def projects(self) -> str:
        """Gets information about Daniel Avila's projects"""
        data = self._fetch_api_data("projects")
        return json.dumps(data, indent=4)

    def contact(self) -> str:
        """Gets Daniel Avila's contact information"""
        data = self._fetch_api_data("contact")
        return json.dumps(data, indent=4)

    def send_contact_message(self, message: str) -> str:
        """Sends a message through the contact form"""
        data = self._post_api_data("contact", {"message": message})
        return json.dumps(data, indent=4)

    def talks(self) -> str:
        """Retrieves information about talks given and community involvement"""
        data = self._fetch_api_data("talks")
        return json.dumps(data, indent=4)

    def skills(self) -> str:
        """Retrieves detailed information about different skill sets"""
        data = self._fetch_api_data("skills")
        return json.dumps(data, indent=4)

    def check_skill(self, skill_name: str) -> str:
        """Checks if Daniel Avila has a specific skill"""
        data = self._fetch_api_data(f"skills/{skill_name}")
        return json.dumps(data, indent=4)
