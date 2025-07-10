def get_files_info(working_directory, directory=None):
    
    abs_working = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))
    
    if abs_dir.startswith(abs_working) == False:
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if os.path.isdir(abs_dir) == False:
        return (f'Error: "{directory}" is not a directory')
    
    dir_list = os.listdir(abs_dir)

    final_result = []

    for item in dir_list:
        item_path = os.path.join(abs_dir, item)

        file_size = os.path.getsize(item_path)
        dir_status = os.path.isdir(item_path)
        
        final_result.append(f"- {item}: file_size={file_size} bytes, is_dir={dir_status}")

    return "\n".join(final_result)