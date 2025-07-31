from google.genai import types
import os
import sys
from functions.get_files_info import schema_get_files_info
from dotenv import load_dotenv
from google import genai
from google.genai import types

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
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

    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
        )
    )
    
    if response.function_calls:
        first_call = response.function_calls[0]
        print(f"Calling function: {first_call.name}({first_call.args})")
    else:

        if verbose == True:
            print("User prompt:")
            print(response.text)
            print("Prompt tokens:")
            print(response.usage_metadata.prompt_token_count)
            print("Response tokens:")
            print(response.usage_metadata.candidates_token_count)
        else:
            print("Response:")
            print(response.text)


if __name__ == "__main__":
    main()
