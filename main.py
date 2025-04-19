"""
This file is the main entry point for the Merlin AI agent.

It is responsible for initializing the agent and executing the main interaction loop
that processes user inputs and displays responses.
"""
import sys
import asyncio

from src.agent.openai_agent import Agent


async def main():
    """
    Main function to run the Merlin AI assistant.

    This function:
    1. Initializes the AI agent
    2. Displays a welcome message
    3. Enters a loop that:
       - Collects user input
       - Processes it through the agent
       - Continues until the user exits
    4. Handles graceful termination

    Note:
        The function runs asynchronously to support the agent's async operations.
        Exit the program by typing 'exit', 'quit', or pressing Ctrl+C.
    """
    try:
        agent = Agent()

        print("\n\nWelcome to Merlin!")
        while True:
            try:
                user_input = input(">>> ")
                if user_input.lower() in ["exit", "quit"]:
                    break
                await agent.run(user_input)
            except (EOFError, KeyboardInterrupt):
                break
            except Exception as e:
                print(f"Error processing input: {str(e)}")
                print("Please try again with a different query.")

        print("Goodbye!")
    except ValueError as e:
        # Handle initialization errors (e.g., from missing env variables)
        print(f"Error initializing Merlin: {str(e)}")
        sys.exit(1)
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
