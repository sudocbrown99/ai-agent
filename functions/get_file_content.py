from config import MAX_CHARS
import os
from google.genai import types

def get_file_content(working_directory, file_path):
        
    abs_working = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([abs_working, abs_file]) != abs_working:
        return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        
    if os.path.isfile(abs_file) == False:
        return (f'Error: File not found or is not a regular file: "{file_path}"')
    
    try:
        with open(abs_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return f"Error: {str(e)}"

    try:
        if os.path.getsize(abs_file) > MAX_CHARS:
            file_content_string += (f'[...File "{file_path}" truncated at 10000 characters]')
    except Exception as e:
        return f"Error: {str(e)}"

    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)