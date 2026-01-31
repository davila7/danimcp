# File: prompts.py
from fastmcp.prompts import Message

class DaniMCPPrompts:
    """Prompts implementation for Daniel Avila's MCP server"""

    @staticmethod
    def about_me_prompt() -> list[Message]:
        """Creates a prompt for getting information about Daniel"""
        return [
            Message("Let me tell you about Daniel Avila:"),
            Message("I'll help you learn more about Daniel. What would you like to know?", role="assistant")
        ]

    @staticmethod
    def tech_prompt(tech: str = None) -> list[Message]:
        """Creates a prompt for technology information"""
        messages = [
            Message("Let's explore Daniel's technical expertise:")
        ]
        if tech:
            messages.append(Message(f"Tell me about his experience with {tech}"))
        messages.append(Message("I'll help you understand his technical background.", role="assistant"))
        return messages
