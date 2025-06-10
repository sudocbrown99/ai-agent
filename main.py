import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


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
    )
    
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
