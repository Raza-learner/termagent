import os
import time
import argparse
from google.genai import types
from dotenv import load_dotenv
from google import genai
from config import system_prompt


def response():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    try:
        if args.verbose:
            usage = response.usage_metadata
            print(f"User Prompt:{user_prompt}")
            print(f"Prompt tokens:{usage.prompt_token_count}")
            print(f"Response tokens:{usage.candidates_token_count}")
            print(response.text)
        else:
            print(response.text)
    except RuntimeError as e:
        print(f"Gemini API response appears to be malformed{e}")


def main() -> None:
    response()


if __name__ == "__main__":
    main()
