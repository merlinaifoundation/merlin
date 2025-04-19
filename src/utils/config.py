"""
This file contains the configuration loader.

It is responsible for loading and providing access to the application's configuration.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Manages application configuration settings loaded from environment variables.

    This class centralizes all configuration settings for the application,
    mainly loaded from environment variables (typically set in a .env file).
    It provides both direct settings (like API keys) and computed properties
    (like the directories mapping).

    Attributes:
        OPENAI_API_KEY (str): OpenAI API key for authentication
        MODEL_NAME (str): The OpenAI model to use for completions
        SYSTEM_PROMPT (str): The default system prompt for the agent
        FUZZY_SEARCH_THRESHOLD (int): Minimum score (0-100) for fuzzy search matches
        DEFAULT_SEARCH_RESULTS (int): Default number of results to return from searches
    """
    # API keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

    # Model settings
    DEFAULT_MODEL_NAME = "gpt-4o"
    MODEL_NAME = os.getenv("MODEL_NAME", "") or DEFAULT_MODEL_NAME

    # System prompt - Always set a default value if not provided or empty
    DEFAULT_SYSTEM_PROMPT = """You are an autonomous developer agent. Follow the user's goal using an explicit multi‑step plan. Each step must be atomic (one terminal command or one tool call)."""
    SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "") or DEFAULT_SYSTEM_PROMPT

    # Search settings
    FUZZY_SEARCH_THRESHOLD = int(os.getenv("FUZZY_SEARCH_THRESHOLD", "60"))
    DEFAULT_SEARCH_RESULTS = int(os.getenv("DEFAULT_SEARCH_RESULTS", "3"))

    def __init__(self):
        """
        Initialize the configuration and validate required variables.

        Raises:
            SystemExit: If any required configuration variables are missing
        """
        self.validate_config()
        print(f"- Using model: {self.MODEL_NAME}")
        if os.getenv("SYSTEM_PROMPT", "").strip() == "":
            print("- Using default system prompt")

        # Log available directories
        dirs = self.directories
        if len(dirs) <= 1:  # Only cwd is available
            print("- WARNING: No custom directories configured. Agent only has access to the current working directory.")
        else:
            print(f"- Agent has access to {len(dirs)} directories:")
            for name, path in dirs.items():
                print(f"  - {name}: {path}")

        # Log exit instructions
        print("- Type 'exit' or press Ctrl+C to quit")

    def validate_config(self):
        """
        Validate that all required configuration variables are present.

        This method checks if critical environment variables are set
        and exits the program with an error message if any are missing.

        Raises:
            SystemExit: If any required configuration variables are missing
        """
        missing_vars = []

        # Check required API keys
        if not self.OPENAI_API_KEY:
            missing_vars.append("OPENAI_API_KEY")

        # Validate directories
        dir_vars = self._get_directory_vars()
        if dir_vars:
            invalid_dirs = []
            for key, value in dir_vars.items():
                if not os.path.isdir(value):
                    invalid_dirs.append(
                        f"{key}={value} (directory does not exist)")

            if invalid_dirs:
                print(
                    "Warning: The following directory variables point to non-existent paths:")
                for invalid_dir in invalid_dirs:
                    print(f"  - {invalid_dir}")

        # Exit if required variables are missing
        if missing_vars:
            print("Error: The following required environment variables are missing:")
            for var in missing_vars:
                print(f"  - {var}")
            print(
                "\nPlease set these variables in your .env file or environment and try again.")
            sys.exit(1)

    def _get_directory_vars(self):
        """
        Get all directory environment variables.

        Returns:
            dict: Dictionary of environment variables ending with _DIR
        """
        return {k: v for k, v in os.environ.items()
                if k.startswith("MERLIN_DIR_") and v}

    @property
    def directories(self):
        """
        Gets configured directories from the .env file.

        This property scans environment variables for any ending with '_DIR',
        validates that they point to existing directories, and creates a mapping
        from a simplified name to the directory path.

        Only includes specifically configured directories plus the current
        working directory.

        Returns:
            dict: A dictionary mapping directory aliases (lowercase names) to their absolute paths

        Example:
            If HOME_DIR=/home/user is in .env, this will return {'home': '/home/user', 'cwd': '/current/dir'}
        """
        dirs = {}
        for key, value in self._get_directory_vars().items():
            if os.path.isdir(value):
                # Converts "MERLIN_DIR_WORK" to "work"
                name = key.replace("MERLIN_DIR_", "").lower()
                dirs[name] = value

        # Always include the current working directory
        dirs["cwd"] = os.getcwd()

        return dirs


# Singleton instance
config = Config()
