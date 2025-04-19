"""
This file contains the tool definitions for the agent.

It centralizes all tool configurations in one place for easier maintenance.
"""

# Define tools available to the agent
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_commands",
            "description": "Run shell commands.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commands": {"type": "array",
                                 "items": {"type": "string"}},
                    "background": {"type": "boolean"}
                },
                "required": ["commands"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "vector_search",
            "description": "Return absolute paths that match a query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer"}
                },
                "required": ["query"]
            }
        }
    }
]
