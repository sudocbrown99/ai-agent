from google.genai import types
import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    
    abs_working = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    if os.path.commonpath([abs_working, abs_file]) != abs_working:
        return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    
    file_dir = os.path.dirname(abs_file)
    
    if os.path.exists(abs_file) == False:
        return (f'Error: File "{file_path}" not found.')
    
    if abs_file.endswith('.py') == False:
        return (f'Error: "{file_path}" is not a Python file.')
    
    try:
        result  = subprocess.run(['python', str(abs_file)] + args, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_directory)
        output_stdout = result.stdout.decode("utf-8")
        output_stderr = result.stderr.decode("utf-8")
        sections = []
        if output_stdout.strip():
            sections.append(f'STDOUT: {output_stdout.strip()}')
        if output_stderr.strip():
            sections.append(f'STDERR: {output_stderr.strip()}')
        if result.returncode != 0:
            sections.append(f'Process exited with code {result.returncode}')
        if not sections:
            return 'No output produced.'
        return ' '.join(sections)
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments, constrained to the working directory.",
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
