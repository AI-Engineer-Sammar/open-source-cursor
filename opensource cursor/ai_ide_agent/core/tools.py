import os
import subprocess

def read_file_content(file_path: str) -> str:
    """Reads and returns the content of a specified file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file_content(file_path: str, content: str) -> str:
    """Writes or overwrites content to a specified file."""
    try:
        abs_path = os.path.abspath(file_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully created/updated file: '{file_path}'"
    except Exception as e:
        return f"Error writing file '{file_path}': {str(e)}"

def list_workspace_files(directory_path: str = ".") -> str:
    """Lists files and directories inside the workspace."""
    try:
        abs_dir = os.path.abspath(directory_path)
        files_list = []
        for root, dirs, files in os.walk(abs_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), abs_dir)
                files_list.append(rel_path)
        return "\n".join(files_list) if files_list else "Directory is currently empty."
    except Exception as e:
        return f"Error listing files: {str(e)}"

def execute_terminal_command(command: str) -> str:
    """Executes a bash terminal command and returns output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout if result.stdout else result.stderr
        return output if output else "Command executed with no output."
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 60 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"

AGENT_TOOLS = [
    read_file_content,
    write_file_content,
    list_workspace_files,
    execute_terminal_command
]

def execute_tool_call(tool_name: str, tool_args: dict, project_folder: str = ".") -> str:
    """Dispatches tool call execution dynamically with absolute paths."""
    try:
        abs_project_folder = os.path.abspath(project_folder)

        if "file_path" in tool_args:
            path = tool_args["file_path"]
            if not os.path.isabs(path):
                tool_args["file_path"] = os.path.join(abs_project_folder, path)

        if tool_name == "read_file_content":
            return read_file_content(**tool_args)
        elif tool_name == "write_file_content":
            return write_file_content(**tool_args)
        elif tool_name == "list_workspace_files":
            if "directory_path" not in tool_args or tool_args["directory_path"] == ".":
                tool_args["directory_path"] = abs_project_folder
            return list_workspace_files(**tool_args)
        elif tool_name == "execute_terminal_command":
            return execute_terminal_command(**tool_args)
        else:
            return f"Error: Unknown tool function '{tool_name}'"
    except Exception as e:
        return f"Error executing tool {tool_name}: {str(e)}"
