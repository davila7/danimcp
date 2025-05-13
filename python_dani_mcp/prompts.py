# File: prompts.py
from mcp.server.fastmcp.prompts import base
from typing import List

class DaniMCPPrompts:
    """Prompts implementation for Daniel Avila's MCP server"""
    
    @staticmethod
    def about_me_prompt() -> List[base.Message]:
        """Creates a prompt for getting information about Daniel"""
        return [
            base.UserMessage("Let me tell you about Daniel Avila:"),
            base.AssistantMessage("I'll help you learn more about Daniel. What would you like to know?")
        ]
    
    @staticmethod
    def tech_prompt(tech: str = None) -> List[base.Message]:
        """Creates a prompt for technology information"""
        messages = [
            base.UserMessage("Let's explore Daniel's technical expertise:")
        ]
        if tech:
            messages.append(base.UserMessage(f"Tell me about his experience with {tech}"))
        messages.append(base.AssistantMessage("I'll help you understand his technical background."))
        return messages