"""
This file contains the agent state.

It is responsible for managing the state of the agent.
"""
import os
from pathlib import Path


class AgentState:
    """
    Manages the runtime state of the agent throughout its lifecycle.

    This class maintains the conversation history, working directory,
    and other stateful information needed for the agent to function
    across multiple interactions.

    Attributes:
        working_dir (str): The current working directory for command execution
        messages (list): The full message history for the OpenAI API
        last_command_result (str): Output from the most recently executed command
        conversation_history (list): Tuples of (role, content) for the conversation
    """

    def __init__(self):
        """
        Initialize a new AgentState with default values.

        Sets the working directory to the current directory and
        initializes empty collections for messages and history.
        """
        self.working_dir = os.getcwd()
        self.messages = []
        self.last_command_result = None
        self.conversation_history = []

    def reset(self):
        """
        Reset the agent's conversation state while preserving the working directory.

        This method clears the message history and last command result,
        but does not change the current working directory.

        Returns:
            None
        """
        self.messages = []
        self.last_command_result = None

    def update_working_dir(self, new_dir):
        """
        Update the agent's working directory if the path exists.

        This method changes the working directory used for command execution
        after validating that the provided path exists and is a directory.

        Args:
            new_dir (str): The new directory path (can be relative or use ~)

        Returns:
            bool: True if the working directory was updated successfully,
                  False if the path doesn't exist or isn't a directory

        Note:
            The path is converted to an absolute path before storage
        """
        path = Path(new_dir).expanduser().resolve()
        if path.exists() and path.is_dir():
            self.working_dir = str(path)
            return True
        return False


# Singleton instance
state = AgentState()
