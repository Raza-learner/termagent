import os
import subprocess
from google.genai import types


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abspath_directory = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abspath_directory, file_path))
        valid_target_dir = (
            os.path.commonpath([abspath_directory, target_directory])
            == abspath_directory
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{file_path}"" as it is outside the permitted working directory'

        if not os.path.isfile(target_directory):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_directory.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_directory]

        if args:
            command.extend(args)

        process = subprocess.run(
            command, cwd=abspath_directory, capture_output=True, text=True, timeout=30
        )

        output = ""
        if process.stdout:
            output += process.stdout
            return f"STDOUT:{output}"
        if process.stderr:
            output += process.stderr
            return f"STDERR:{output}"
        if not output:
            return "No output produced"

        if process.returncode != 0:
            output = f"Process exited with code {process.returncode}\n" + output
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run files with .py",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="This will work for file path",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the script.",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)
