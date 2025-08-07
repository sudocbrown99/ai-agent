from google.genai import types
import os
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
        schema_get_file_content,
    ]
)

def main():
    load_dotenv()

    args = sys.argv[1:]
    verbose = "--verbose" in args
    filtered_args = [arg for arg in args if arg != "--verbose"]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(filtered_args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(20):
        try:
            messages, response = generate_content(client, messages, verbose)

            if response.text and not response.function_calls:
                print("Final response:")
                print(response.text)
                break
        
        except Exception as e:
            print(f"Error: {e}")
            break

def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
        )
    )

    for candidate in response.candidates:
        messages.append(candidate.content)
    
    if response.function_calls:
        first_call = response.function_calls[0]
        function_call_result = call_function(first_call, verbose)

        if not function_call_result.parts or not hasattr(function_call_result.parts[0], "function_response"):
            raise Exception("Function response missing")
        
        result = function_call_result.parts[0].function_response.response
        messages.append(types.Content(role="tool", parts=[function_call_result.parts[0]]))
        if verbose:
            print(f"-> {result}")
        else:
            print(result)
    
    return messages, response


if __name__ == "__main__":
    main()