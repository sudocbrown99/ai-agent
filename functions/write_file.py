import os
from google.genai import types

def write_file(working_directory, file_path, content):

    abs_working = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))


    if os.path.commonpath([abs_working, abs_file]) != abs_working:
        return (f'Error: Cannot write "{file_path}" as it is outside the permitted working directory')
    
    file_dir = os.path.dirname(abs_file)
    if os.path.exists(file_dir) == False:
        os.makedirs(file_dir)
    
    try:
        with open(abs_file, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {str(e)}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)