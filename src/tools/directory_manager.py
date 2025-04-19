"""
This file contains the directory manager tool.

It is responsible for tracking and managing directories available to the agent.
"""
import os
from pathlib import Path

from src.utils.config import config


class DirectoryManager:
    """
    Manages the directories accessible to the agent.

    This class provides a central registry of directories that the agent
    is allowed to access, helping to enforce security boundaries.
    It allows adding new directories, retrieving directory paths by alias,
    and listing all managed directories.

    Attributes:
        directories (dict): A dictionary mapping directory aliases to absolute paths
    """

    def __init__(self):
        """
        Initialize the DirectoryManager with directories from configuration.

        The directories are loaded from the configuration object, which
        typically reads them from environment variables in .env file.
        """
        # Only uses directories defined in .env
        self.directories = config.directories

    def get_all_directories(self) -> str:
        """
        Return a formatted string listing all managed directories.

        This method generates a human-readable string representation
        of all managed directories, with one directory per line in
        the format "alias: path".

        Returns:
            str: A newline-separated string of directory aliases and paths,
                 or a message indicating no directories are configured.

        Example:
            >>> directory_manager.get_all_directories()
            "home: /home/user\nwork: /path/to/work\ncwd: /current/directory"
        """
        if not self.directories:
            return "No specific directories configured."
        return "\n".join(f"{k}: {v}" for k, v in self.directories.items())

    def add_directory(self, name, path):
        """
        Add a new directory to the managed directories.

        This method registers a new directory with the specified alias,
        after validating that the path exists and is a directory.

        Args:
            name (str): The alias to use for the directory
            path (str): The path to the directory (can be relative or use ~)

        Returns:
            bool: True if the directory was successfully added,
                  False if the path doesn't exist or isn't a directory

        Note:
            The path is converted to an absolute path before storage
        """
        abs_path = str(Path(path).expanduser().resolve())
        if os.path.isdir(abs_path):
            self.directories[name] = abs_path
            return True
        return False

    def get_directory(self, name):
        """
        Get a directory's absolute path by its alias.

        Args:
            name (str): The alias of the directory to retrieve

        Returns:
            str or None: The absolute path of the directory if found,
                        None if the alias doesn't exist

        Example:
            >>> directory_manager.get_directory("home")
            "/home/user"
        """
        return self.directories.get(name)


# Singleton instance
directory_manager = DirectoryManager()
