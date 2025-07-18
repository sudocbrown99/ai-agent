from config import MAX_CHARACTERS
import os

def get_file_content(working_directory, file_path):
        
        abs_working = os.path.abspath(working_directory)
        abs_file = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([abs_working, abs_file]) != abs_working:
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        
        if os.path.isfile(abs_file) == False:
            return (f'Error: File not found or is not a regular file: "{file_path}"')
        
