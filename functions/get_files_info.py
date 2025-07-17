import os

def get_files_info(working_directory, directory="."):
    
    abs_working = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))
    
    if os.path.commonpath([abs_working, abs_dir]) != abs_working:
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if os.path.isdir(abs_dir) == False:
        return (f'Error: "{directory}" is not a directory')
    
    try:
        dir_list = os.listdir(abs_dir)
    except Exception as e:
        return f"Error: {str(e)}"

    final_result = []

    for item in dir_list:
        item_path = os.path.join(abs_dir, item)
        try:
            file_size = os.path.getsize(item_path)
            dir_status = os.path.isdir(item_path)
            final_result.append(f" - {item}: file_size={file_size} bytes, is_dir={dir_status}")
        except Exception as e:
            return f"Error: {str(e)}"
        


    return "\n".join(final_result)

    