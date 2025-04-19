"""
This file contains the OpenAI agent.

It is responsible for interacting with the OpenAI API.
"""
import json
from openai import AsyncOpenAI

from src.agent.agent_state import state
from src.tools.directory_manager import directory_manager
from src.tools.command_executor import execute_commands
from src.tools.vector_search import search as vector_search
from src.utils.config import config
from src.utils.tools_config import TOOLS

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)


class Agent:
    """
    Agent class for interacting with the OpenAI API.
    """

    def __init__(self):
        """
        Initialize the agent with system prompt and directory information.

        Raises:
            ValueError: If MODEL_NAME is not set in the .env file
        """
        if not config.MODEL_NAME:
            raise ValueError("ERROR: MODEL_NAME must be set in .env file")

        # Create the system prompt including configured directories
        base_prompt = config.SYSTEM_PROMPT.strip()
        directory_info = directory_manager.get_all_directories()

        if base_prompt:
            self.system_prompt = f"{base_prompt}\n\nKnown directories:\n{directory_info}"
        else:
            self.system_prompt = f"You are a terminal assistant.\n\nKnown directories:\n{directory_info}"

    async def run(self, user_text: str):
        """
        Process a user message and generate a response using the OpenAI API.

        This method handles the complete interaction cycle:
        1. Adding the user message to the conversation history
        2. Sending the conversation to the OpenAI API
        3. Processing any tool calls requested by the model
        4. Handling the model's text response
        5. Updating the conversation history

        Args:
            user_text (str): The user's input text message

        Returns:
            None: The response is printed to the console

        Side Effects:
            - Updates the agent's state and conversation history
            - Executes commands if requested by the model
            - Prints the model's response to the console
        """
        # Add system message on first turn
        if not state.messages:
            state.messages.append(
                {"role": "system", "content": self.system_prompt}
            )

        # Add user message
        state.messages.append({"role": "user", "content": user_text})
        state.conversation_history.append(("user", user_text))

        # Main interaction loop
        while True:
            try:
                # Get response from OpenAI
                rsp = await client.chat.completions.create(
                    model=config.MODEL_NAME,
                    messages=list(state.messages),
                    tools=TOOLS,
                    tool_choice="auto"
                )
                msg = rsp.choices[0].message

                # Handle tool calls
                if msg.tool_calls:
                    tool_call_msgs = []

                    for call in msg.tool_calls:
                        fn_name = call.function.name
                        args = json.loads(call.function.arguments or "{}")

                        if fn_name == "execute_commands":
                            output = await execute_commands(**args)
                        elif fn_name == "vector_search":
                            paths = vector_search(**args)
                            output = json.dumps(paths)
                        else:
                            output = f"Unknown tool {fn_name}"

                        tool_call_msgs.append({
                            "role": "tool",
                            "tool_call_id": call.id,
                            "name": fn_name,
                            "content": output
                        })

                    # Add assistant message and tool responses
                    state.messages.append({
                        "role": "assistant",
                        "content": msg.content,
                        "tool_calls": msg.tool_calls
                    })
                    state.messages.extend(tool_call_msgs)

                    # Continue loop to feed results back to model
                    continue

                # Handle plain text reply
                content = msg.content.strip()
                print(content)

                # Save to conversation history
                state.messages.append(
                    {"role": "assistant", "content": content})
                state.conversation_history.append(("assistant", content))

                break  # End the turn

            except Exception as e:
                print(f"Error: {str(e)}")
                break
