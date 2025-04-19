"""
This file contains the command executor tool.

It is responsible for executing shell commands.
"""
import asyncio
import shlex
from pathlib import Path

from src.agent.agent_state import state


async def _run(cmd: str):
    """
    Run a single shell command in the current working directory.

    This is an internal helper function used by execute_commands
    to run individual commands in the agent's current working directory.

    Args:
        cmd (str): The shell command to execute

    Returns:
        tuple: A 3-tuple containing:
            - return_code (int): The exit code of the command (0 for success)
            - stdout (str): The standard output of the command
            - stderr (str): The standard error output of the command

    Note:
        Uses asyncio.create_subprocess_shell for asynchronous execution
    """
    process = await asyncio.create_subprocess_shell(
        cmd,
        cwd=state.working_dir,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()


async def execute_commands(commands: list[str], background: bool = False):
    """
    Execute shell commands sequentially and return their results.

    This function handles multiple commands, executing them in order and
    collecting their outputs. It has special handling for 'cd' commands
    to update the agent's working directory state.

    Args:
        commands (list[str]): List of command strings to execute
        background (bool, optional): Whether to run commands in background
                                     without waiting for their completion.
                                     Defaults to False.

    Returns:
        str: A string containing the aggregated results of all commands,
             separated by double newlines. For background commands,
             just confirms they were started.

    Side Effects:
        - May change the agent's working directory (state.working_dir)
        - Updates state.last_command_result with the most recent command output
        - For background commands, starts processes detached from the main process

    Example:
        >>> await execute_commands(["ls -la", "echo hello"])
        "$ ls -la\nexit=0\nstdout:\nfile1 file2...\nstderr:\n\n$ echo hello\nexit=0\nstdout:\nhello\nstderr:\n"
    """
    aggregated = []

    for raw in commands:
        # Handle cd command specially
        if raw.startswith("cd "):
            # Update working dir locally; no subprocess needed
            target = Path(shlex.split(raw)[1]).expanduser().resolve()
            if target.exists() and target.is_dir():
                state.working_dir = str(target)
                aggregated.append(f"Changed directory to {target}")
            else:
                aggregated.append(f"Directory not found: {target}")
            continue

        # Execute regular commands
        if background:
            await asyncio.create_subprocess_shell(
                raw,
                cwd=state.working_dir,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
                start_new_session=True
            )
            aggregated.append(f"Started in background: {raw}")
        else:
            code, out, err = await _run(raw)
            result = f"$ {raw}\nexit={code}\nstdout:\n{out}\nstderr:\n{err}"
            aggregated.append(result)
            state.last_command_result = result

    return "\n\n".join(aggregated)
