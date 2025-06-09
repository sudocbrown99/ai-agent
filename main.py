import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    if len(sys.argv) == 1:
        print("Must provide an input")
        sys.exit(1)

    user_input = sys.argv[1]
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=user_input
    )   
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
