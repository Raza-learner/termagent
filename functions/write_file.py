import os
from google.genai import types


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abspath_directory = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abspath_directory, file_path))

        valid_target_dir = (
            os.path.commonpath([abspath_directory, target_directory])
            == abspath_directory
        )

        if not valid_target_dir:
            return f"Error: Cannot list {file_path} as it is outside the permitted working directory"

        if os.path.isdir(target_directory):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_directory), exist_ok=True)

        with open(target_directory, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error:{e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Edit files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
