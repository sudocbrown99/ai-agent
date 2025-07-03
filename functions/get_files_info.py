def get_files_info(working_directory, directory=None):
    
    abs_working = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))
    
    if abs_dir.startswith(abs_working) == False:
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if os.path.isdir(directory) == False:
        return (f'Error: "{directory}" is not a directory')