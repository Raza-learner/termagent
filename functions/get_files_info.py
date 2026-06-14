import os
from google.genai import types


def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        abspath_directory = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abspath_directory, directory))

        valid_target_dir = (
            os.path.commonpath([abspath_directory, target_directory])
            == abspath_directory
        )

        if not valid_target_dir:
            return f"Error: Cannot list {directory} as it is outside the permitted working directory"

        if not os.path.isdir(target_directory):
            return f"Error: {directory} is not a directory"

        result = []
        for item in os.listdir(target_directory):
            name = os.path.join(target_directory, item)
            size = os.path.getsize(name)
            dir_exist = os.path.isdir(item)
            result.append(f"- {name}: file_size={size} bytes, is_dir={dir_exist}")
        return "\n".join(result)

    except Exception as e:
        return f"Error:{e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


# test = get_files_info("calculator")
# print(test)
