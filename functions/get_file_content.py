import os
from config import MAX_CHARS
from functions.get_files_info import get_files_info

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abspath_directory = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abspath_directory,file_path))
    
        valid_target_dir = os.path.commonpath([abspath_directory, target_directory]) == abspath_directory 
        

        if not valid_target_dir :
            return f"Error: Cannot list {file_path} as it is outside the permitted working directory"

        if not os.path.isfile(target_directory):
            return f'Error: File not found or is not a regular file: "{file_path}"'
            
        with open(target_directory, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += f'[...file "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string

    except Exception as e:
        return f"Error:{e}" 



